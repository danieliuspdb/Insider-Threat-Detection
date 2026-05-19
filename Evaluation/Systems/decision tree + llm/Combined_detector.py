import pandas as pd
import numpy as np
import joblib
import os
import re
import math
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from accelerate import dispatch_model, infer_auto_device_map

BASE = '..'
DT_MODEL = 'Path'
DT_TEST = 'Path'
INSIDERS_FILE = 'Path'
EMAILS_FILE = 'Path'
HTTP_FILE = 'Path'
KEYWORDS_FILE = 'Path'

LORA_ADAPTER_PATH = 'Path'
BASE_MODEL_NAME = 'Path'
OFFLOAD_DIR = r".\offload"
os.makedirs(OFFLOAD_DIR, exist_ok=True)
MAX_MEMORY = {0: "4GiB", "cpu": "16GiB"}

INSTRUCTION = "You are a security analyst. Classify the following message."
LABELS = [
    "BENIGN", "DATA_EXFILTRATION", "IP_THEFT", "EMPLOYEE_POACHING",
    "CONFLICT_OF_INTEREST", "POLICY_CIRCUMVENTION", "FINANCIAL_FRAUD",
    "CREDENTIAL_ABUSE", "UNION_ORGANIZING", "STRESSED_EMPLOYEE", "JOB_SEEKING",
]
LABEL_SET = set(LABELS)
CONFIDENCE_THRESHOLD = 0.84

def build_prompt(message: str) -> str:
    return f"""### Instruction:
{INSTRUCTION}
Classify the following message using ONLY ONE label from this list and do not use any labels not from here:
{", ".join(LABELS)}

### Input:
{message}

### Response:
"""

def extract_label(text: str) -> str:
    cleaned = text.strip().upper()
    first_line = cleaned.splitlines()[0].strip()
    first_line = re.sub(r"[^A-Z_]", "", first_line)
    if first_line in LABEL_SET:
        return first_line
    for lab in LABELS:
        if lab in cleaned:
            return lab
    return "UNKNOWN"

def load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    )

    model = PeftModel.from_pretrained(base, LORA_ADAPTER_PATH)
    model = model.merge_and_unload()

    device_map = infer_auto_device_map(model, max_memory=MAX_MEMORY)
    model = dispatch_model(model, device_map=device_map, offload_dir=OFFLOAD_DIR)

    model.eval()
    model.config.use_cache = False
    return model, tokenizer

def generate_label_and_confidence(model, tokenizer, prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=20,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            output_scores=True,
            return_dict_in_generate=True,
        )

    num_input_tokens = inputs.input_ids.shape[1]
    gen_ids = outputs.sequences[0, num_input_tokens:]

    token_probs = []
    for i, token_id in enumerate(gen_ids):
        if i >= len(outputs.scores):
            break
        logits = outputs.scores[i][0]
        probs = torch.softmax(logits, dim=-1)
        p = probs[token_id].item()
        token_probs.append(p)

        tok_text = tokenizer.decode([token_id])
        if tok_text.strip() in ["", "\n"] or token_id == tokenizer.eos_token_id:
            break

    if token_probs:
        log_sum = sum(math.log(p) for p in token_probs if p > 0)
        confidence = math.exp(log_sum / len(token_probs))
    else:
        confidence = 0.0

    decoded = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
    response_text = decoded.split("### Response:")[-1].strip()
    predicted_label = extract_label(response_text)

    return predicted_label, confidence


insiders_df = pd.read_csv(INSIDERS_FILE)
all_insiders_from_file = set(insiders_df['user'].astype(str).unique())

model_data = joblib.load(DT_MODEL)
dt_model = model_data['model']
feature_names = model_data['feature_names']
threshold = model_data['threshold']

test_df = pd.read_excel(DT_TEST)
test_users = test_df['user'].values
print(f"  Test users: {len(test_users)}")

X_test = test_df[feature_names].values
dt_probs = dt_model.predict_proba(X_test)[:, 1]
dt_preds = (dt_probs >= threshold).astype(int)

dt_flagged = set(test_users[dt_preds == 1])
print(f"  Decision Tree flagged: {len(dt_flagged)} users")

true_insiders = all_insiders_from_file & set(test_users)
print(f"  True insiders in test set: {len(true_insiders)}")

with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
    keywords = [line.strip() for line in f if line.strip() and not line.startswith('#')]
print(f"  Loaded {len(keywords)} keywords")

email_df = pd.read_excel(EMAILS_FILE)
http_df = pd.read_excel(HTTP_FILE)
print(f"  Loaded {len(email_df)} emails, {len(http_df)} HTTP records")

keyword_matched = set()

for user in test_users:
    user_email = email_df[email_df['user'] == user]
    user_http = http_df[http_df['user'] == user]

    matched = False

    for _, email in user_email.iterrows():
        content = str(email['content']).lower()
        if any(keyword.lower() in content for keyword in keywords):
            matched = True
            break

    if not matched:
        for _, http in user_http.iterrows():
            content = str(http['content']).lower()
            url = str(http['url']).lower()
            if any(keyword.lower() in content or keyword.lower() in url for keyword in keywords):
                matched = True
                break

    if matched:
        keyword_matched.add(user)

print(f"  Keyword matched: {len(keyword_matched)} users")

model, tokenizer = load_model_and_tokenizer()
print("  LLM loaded")

llm_flagged = set()

for idx, user in enumerate(sorted(keyword_matched), 1):
    user_email = email_df[email_df['user'] == user]
    user_http = http_df[http_df['user'] == user]

    messages = []
    if len(user_email) > 0:
        email_content = str(user_email.iloc[0]['content'])[:300]
        messages.append(f"EMAIL: {email_content}")
    if len(user_http) > 0:
        http_content = str(user_http.iloc[0]['content'])[:300]
        messages.append(f"HTTP: {http_content}")

    combined_message = "\n".join(messages)
    prompt = build_prompt(combined_message)
    pred_label, confidence = generate_label_and_confidence(model, tokenizer, prompt)

    is_anomaly = (pred_label != "BENIGN")

    if is_anomaly and confidence >= CONFIDENCE_THRESHOLD:
        llm_flagged.add(user)
        status = "FLAGGED"
    else:
        status = f"rejected ({pred_label}, {confidence*100:.1f}%)"

    print(f"  [{idx}/{len(keyword_matched)}] {user}: {status}", flush=True)

print(f"\n  LLM flagged: {len(llm_flagged)} users")

all_flagged = dt_flagged | llm_flagged

tp = len(all_flagged & true_insiders)
fp = len(all_flagged - true_insiders)
fn = len(true_insiders - all_flagged)
tn = len(set(test_users) - true_insiders - all_flagged)

total_test = len(test_users)
total_insiders = len(true_insiders)
total_benign = total_test - total_insiders

recall = 100 * tp / total_insiders if total_insiders else 0
precision = 100 * tp / len(all_flagged) if all_flagged else 0
fp_rate = 100 * fp / total_benign if total_benign else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

print("\n" + "="*70)
print("COMBINED RESULTS")
print("="*70)

print(f"\nTotal test users: {total_test}")
print(f"True insiders: {total_insiders}")
print(f"True benign: {total_benign}")

print(f"\n--- METHOD BREAKDOWN ---")
print(f"Decision Tree flagged: {len(dt_flagged)}")
print(f"  TP: {len(dt_flagged & true_insiders)}, FP: {len(dt_flagged - true_insiders)}")

print(f"\nKeyword+LLM flagged: {len(llm_flagged)}")
print(f"  TP: {len(llm_flagged & true_insiders)}, FP: {len(llm_flagged - true_insiders)}")

print(f"\nCombined (DT OR LLM): {len(all_flagged)}")

print(f"\n--- CONFUSION MATRIX ---")
print(f"True Positives (TP):  {tp}")
print(f"False Positives (FP): {fp}")
print(f"False Negatives (FN): {fn}")
print(f"True Negatives (TN):  {tn}")

print(f"\n--- PERFORMANCE METRICS ---")
print(f"Recall (Insiders Caught): {recall:.1f}% ({tp}/{total_insiders})")
print(f"Precision:                {precision:.1f}% ({tp}/{len(all_flagged)})")
print(f"False Positive Rate:      {fp_rate:.1f}% ({fp}/{total_benign})")
print(f"F1 Score:                 {f1:.1f}%")

dt_recall = 100 * len(dt_flagged & true_insiders) / total_insiders if total_insiders else 0
llm_recall = 100 * len(llm_flagged & true_insiders) / total_insiders if total_insiders else 0

print(f"\n--- IMPROVEMENT ANALYSIS ---")
print(f"Decision Tree alone:  {dt_recall:.1f}% recall")
print(f"Keyword+LLM alone:    {llm_recall:.1f}% recall")
print(f"Combined:             {recall:.1f}% recall")
print(f"Gain from combining:  +{recall - dt_recall:.1f}%")

dt_only = dt_flagged & true_insiders - llm_flagged
llm_only = llm_flagged & true_insiders - dt_flagged
both = dt_flagged & llm_flagged & true_insiders

print(f"\n--- INSIDER COVERAGE ---")
print(f"Caught by DT only:      {len(dt_only)}")
print(f"Caught by LLM only:     {len(llm_only)}")
print(f"Caught by both:         {len(both)}")
print(f"Missed by both:         {fn}")

if llm_only:
    print(f"\n--- INSIDERS CAUGHT BY LLM (missed by DT) ---")
    for user in sorted(llm_only)[:10]:
        print(f"  {user}")

missed = true_insiders - all_flagged
if missed:
    print(f"\n--- MISSED INSIDERS ({len(missed)}) ---")
    for user in sorted(missed)[:10]:
        print(f"  {user}")

results_df = pd.DataFrame({
    'user': test_users,
    'is_insider': [u in true_insiders for u in test_users],
    'flagged_by_dt': [u in dt_flagged for u in test_users],
    'flagged_by_llm': [u in llm_flagged for u in test_users],
    'flagged_combined': [u in all_flagged for u in test_users]
})
results_df.to_excel('combined_results.xlsx', index=False)

summary_df = pd.DataFrame([{
    'method': 'combined',
    'total_users': total_test,
    'insiders': total_insiders,
    'flagged': len(all_flagged),
    'tp': tp,
    'fp': fp,
    'tn': tn,
    'fn': fn,
    'precision': precision,
    'recall': recall,
    'fp_rate': fp_rate,
    'f1_score': f1,
    'dt_flagged': len(dt_flagged),
    'llm_flagged': len(llm_flagged)
}])
summary_df.to_excel('combined_summary.xlsx', index=False)