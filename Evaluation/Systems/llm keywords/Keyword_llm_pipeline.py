import pandas as pd
import os
import re
import math
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from accelerate import dispatch_model, infer_auto_device_map

BASE = '..'
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

CONFIDENCE_THRESHOLD = 0.94 

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

email_df_temp = pd.read_excel(EMAILS_FILE)
http_df_temp = pd.read_excel(HTTP_FILE)
dataset_users = set(email_df_temp['user'].unique()) | set(http_df_temp['user'].unique())

true_insiders = all_insiders_from_file & dataset_users
print(f"  {len(all_insiders_from_file)}, but only {len(true_insiders)} exist in email/HTTP datasets)")

with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
    keywords = [line.strip() for line in f if line.strip() and not line.startswith('#')]

email_df = pd.read_excel(EMAILS_FILE)
http_df = pd.read_excel(HTTP_FILE)
all_users = sorted(set(email_df['user'].unique()) | set(http_df['user'].unique()))
print(f"Total users to check: {len(all_users)}")

keyword_matched = set()

for user in all_users:
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

print(f"Users matched by keywords: {len(keyword_matched)}")

model, tokenizer = load_model_and_tokenizer()

llm_confirmed = set()
llm_details = {}

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
    llm_details[user] = {
        'label': pred_label,
        'confidence': confidence,
        'is_anomaly': is_anomaly
    }

    if is_anomaly and confidence >= CONFIDENCE_THRESHOLD:
        llm_confirmed.add(user)
        status = "CONFIRMED INSIDER"
    else:
        status = f"rejected ({pred_label}, {confidence*100:.1f}%)"

    print(f"  [{idx}/{len(keyword_matched)}] {user}: {status}", flush=True)

print(f"\nLLM confirmed insiders: {len(llm_confirmed)}")

tp = len(llm_confirmed & true_insiders) 
fp = len(llm_confirmed - true_insiders) 
fn = len(true_insiders - llm_confirmed) 
tn = len(all_users) - len(true_insiders) - fp 

total_users = len(all_users)
total_insiders = len(true_insiders)
total_benign = total_users - total_insiders

recall = 100 * tp / total_insiders if total_insiders else 0
precision = 100 * tp / len(llm_confirmed) if llm_confirmed else 0
fp_rate = 100 * fp / total_benign if total_benign else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

print(f"Ground truth insiders: {total_insiders}")
print(f"Ground truth benign: {total_benign}")

print(f"Users matched by keywords: {len(keyword_matched)}")
print(f"  True insiders in matches: {len(keyword_matched & true_insiders)}")
print(f"  Benign in matches: {len(keyword_matched - true_insiders)}")

print(f"LLM confirmed insiders: {len(llm_confirmed)}")

print(f"True Positives (TP):  {tp} - Insiders correctly caught")
print(f"False Positives (FP): {fp} - Benign users falsely flagged")
print(f"False Negatives (FN): {fn} - Insiders missed")
print(f"True Negatives (TN):  {tn} - Benign users correctly cleared")

print(f"Recall (Insiders Caught): {recall:.1f}% ({tp}/{total_insiders})")
print(f"Precision:                {precision:.1f}% ({tp}/{len(llm_confirmed)})")
print(f"F1 Score:                 {f1:.1f}%")
print(f"False Positive Rate:      {fp_rate:.1f}% ({fp}/{total_benign})")

if fn > 0:
    missed = true_insiders - llm_confirmed
    print(f"\n--- MISSED INSIDERS ({len(missed)}) ---")
    keyword_missed = missed - keyword_matched
    llm_rejected = missed & keyword_matched

    if keyword_missed:
        print(f"Missed by keywords: {len(keyword_missed)}")
        print(f"  Users: {sorted(keyword_missed)[:10]}")

    if llm_rejected:
        print(f"Matched by keywords but rejected by LLM: {len(llm_rejected)}")
        for user in sorted(llm_rejected)[:5]:
            details = llm_details[user]
            print(f"  {user}: {details['label']} ({details['confidence']*100:.1f}%)")

if fp > 0:
    false_pos = llm_confirmed - true_insiders
    print(f"\n--- FALSE POSITIVES ({len(false_pos)}) ---")
    for user in sorted(false_pos)[:5]:
        details = llm_details[user]
        print(f"  {user}: {details['label']} ({details['confidence']*100:.1f}%)")

caught = llm_confirmed & true_insiders
print(f"\n--- CAUGHT INSIDERS ({len(caught)}) ---")
for user in sorted(caught):
    details = llm_details[user]
    print(f"  {user}: {details['label']} ({details['confidence']*100:.1f}%)")

missed = true_insiders - llm_confirmed
print(f"\n--- MISSED INSIDERS ({len(missed)}) ---")
for user in sorted(missed):
    if user in llm_details:
        details = llm_details[user]
        print(f"  {user}: {details['label']} ({details['confidence']*100:.1f}%) - rejected by LLM")
    elif user in keyword_matched:
        print(f"  {user}: matched keywords but not")
    else:
        print(f"  {user}: no keyword match")