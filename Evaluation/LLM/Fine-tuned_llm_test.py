import os
import re
import json
import math
import time
import torch
import psutil
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from accelerate import dispatch_model, infer_auto_device_map

DATA_PATH = 'Path'
N_SAMPLES = 1000
REPORT_INTERVAL = 20 

LORA_ADAPTER_PATH = 'Path'
BASE_MODEL_NAME = "google/gemma-2-2b-it"

OFFLOAD_DIR = r".\offload"
os.makedirs(OFFLOAD_DIR, exist_ok=True)

MAX_MEMORY = {0: "4GiB", "cpu": "16GiB"}

INSTRUCTION = "You are a security analyst. Classify the following message."

LABELS = [
    "BENIGN",
    "DATA_EXFILTRATION",
    "IP_THEFT",
    "EMPLOYEE_POACHING",
    "CONFLICT_OF_INTEREST",
    "POLICY_CIRCUMVENTION",
    "FINANCIAL_FRAUD",
    "CREDENTIAL_ABUSE",
    "UNION_ORGANIZING",
    "STRESSED_EMPLOYEE",
    "JOB_SEEKING",
]
LABEL_SET = set(LABELS)

NORMALIZE_MAP = {
    "POLICY_CIRCUMENTION": "POLICY_CIRCUMVENTION",
    "POLICY_CIRCUMVENTION": "POLICY_CIRCUMVENTION",
}

def get_gpu_memory_usage():
    if torch.cuda.is_available():
        return {
            "allocated_mb": torch.cuda.memory_allocated() / 1024**2,
            "reserved_mb": torch.cuda.memory_reserved() / 1024**2,
            "max_allocated_mb": torch.cuda.max_memory_allocated() / 1024**2,
        }
    return {"allocated_mb": 0, "reserved_mb": 0, "max_allocated_mb": 0}

def get_system_resources():
    process = psutil.Process()
    return {
        "cpu_percent": process.cpu_percent(interval=0.1),
        "ram_mb": process.memory_info().rss / 1024**2,
        "system_ram_percent": psutil.virtual_memory().percent,
    }

def print_resource_report(idx, total, inference_times, gpu_memory_samples, cpu_samples, ram_samples):
    if not inference_times:
        return

    avg_inference = sum(inference_times) / len(inference_times)
    recent_inference = sum(inference_times[-10:]) / min(10, len(inference_times))

    avg_gpu = sum(gpu_memory_samples) / len(gpu_memory_samples)
    current_gpu = gpu_memory_samples[-1]

    avg_cpu = sum(cpu_samples) / len(cpu_samples)
    current_cpu = cpu_samples[-1]

    avg_ram = sum(ram_samples) / len(ram_samples)
    current_ram = ram_samples[-1]

    print("\n" + "="*70)
    print(f"RESOURCE REPORT - Progress: {idx}/{total} ({idx/total*100:.1f}%)")
    print("="*70)
    print(f"Inference Time:")
    print(f"  Overall Avg:  {avg_inference:.3f}s per sample")
    print(f"  Recent Avg:   {recent_inference:.3f}s per sample (last 10)")
    print(f"GPU Memory (VRAM):")
    print(f"  Current:      {current_gpu:.2f} MB")
    print(f"  Average:      {avg_gpu:.2f} MB")
    print(f"CPU Usage:")
    print(f"  Current:      {current_cpu:.1f}%")
    print(f"  Average:      {avg_cpu:.1f}%")
    print(f"RAM Usage:")
    print(f"  Current:      {current_ram:.2f} MB")
    print(f"  Average:      {avg_ram:.2f} MB")
    print("="*70 + "\n")

def build_prompt(message: str) -> str:
    return f"""### Instruction:
{INSTRUCTION}
Classify the following message using ONLY ONE label from this list and do not use any labels not from here:
{", ".join(LABELS)}

### Input:
{message}

### Response:
"""

def load_dataset(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for i, ex in enumerate(data[:5]):
        if not all(k in ex for k in ("instruction", "input", "output")):
            raise ValueError(f"Example {i} missing required keys. Found keys: {list(ex.keys())}")
    return data

def extract_label(text: str) -> str:
    cleaned = text.strip().upper()

    first_line = cleaned.splitlines()[0].strip()
    first_line = re.sub(r"[^A-Z_]", "", first_line)

    if first_line in NORMALIZE_MAP:
        return NORMALIZE_MAP[first_line]
    if first_line in LABEL_SET:
        return first_line

    for lab in LABELS:
        if lab in cleaned:
            return lab

    if "POLICY_CIRCUMENTION" in cleaned:
        return "POLICY_CIRCUMVENTION"

    return "UNKNOWN"

def load_model_and_tokenizer_once():
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
    start_time = time.time()

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

    inference_time = time.time() - start_time

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

    return predicted_label, confidence, response_text, inference_time

def compute_metrics(results):
    total = len(results)

    correct_label = sum(1 for r in results if r["pred_label"] == r["true_label"])
    label_accuracy = correct_label / total if total else 0.0

    tp = sum(1 for r in results if r["true_anomaly"] and r["pred_anomaly"])
    tn = sum(1 for r in results if (not r["true_anomaly"]) and (not r["pred_anomaly"]))
    fp = sum(1 for r in results if (not r["true_anomaly"]) and r["pred_anomaly"])
    fn = sum(1 for r in results if r["true_anomaly"] and (not r["pred_anomaly"]))

    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0

    return {
        "total": total,
        "label_accuracy": label_accuracy,
        "anomaly_confusion_matrix": {"TP": tp, "TN": tn, "FP": fp, "FN": fn},
        "anomaly_metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "false_positive_rate": fpr,
        },
    }

def main():
    dataset = load_dataset(DATA_PATH)
    subset = dataset[:N_SAMPLES]

    load_start = time.time()
    model, tokenizer = load_model_and_tokenizer_once()
    load_time = time.time() - load_start

    print(f"Model loaded in {load_time:.2f}s")

    initial_gpu = get_gpu_memory_usage()
    initial_sys = get_system_resources()

    print(f"\nInitial GPU Memory: {initial_gpu['allocated_mb']:.2f} MB allocated, {initial_gpu['reserved_mb']:.2f} MB reserved")
    print(f"Initial RAM Usage: {initial_sys['ram_mb']:.2f} MB")

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    results = []
    inference_times = []
    gpu_memory_samples = []
    cpu_samples = []
    ram_samples = []

    for idx, ex in enumerate(subset, start=1):
        message = ex["input"]
        true_label = ex["output"].strip().upper()
        if true_label not in LABEL_SET:
            raise ValueError(f"Unexpected true label: {true_label}")

        prompt = build_prompt(message)
        pred_label, conf, resp, inf_time = generate_label_and_confidence(model, tokenizer, prompt)

        gpu_usage = get_gpu_memory_usage()
        sys_usage = get_system_resources()

        inference_times.append(inf_time)
        gpu_memory_samples.append(gpu_usage['allocated_mb'])
        cpu_samples.append(sys_usage['cpu_percent'])
        ram_samples.append(sys_usage['ram_mb'])

        true_anomaly = (true_label != "BENIGN")
        pred_anomaly = (pred_label != "BENIGN")

        results.append(
            {
                "idx": idx,
                "true_label": true_label,
                "pred_label": pred_label,
                "true_anomaly": true_anomaly,
                "pred_anomaly": pred_anomaly,
                "confidence": conf,
                "raw_model_response": resp[:200].replace("\n", "\\n"),
                "inference_time_sec": inf_time,
            }
        )

        print(
            f"[{idx}/{len(subset)}] true={true_label:20s} pred={pred_label:20s} "
            f"anomaly_true={true_anomaly} anomaly_pred={pred_anomaly} conf={conf*100:.2f}% "
            f"time={inf_time:.3f}s"
        )

        if idx % REPORT_INTERVAL == 0 or idx == 1:
            print_resource_report(idx, len(subset), inference_times, gpu_memory_samples, cpu_samples, ram_samples)

    if len(subset) % REPORT_INTERVAL != 0:
        print_resource_report(len(subset), len(subset), inference_times, gpu_memory_samples, cpu_samples, ram_samples)

    metrics = compute_metrics(results)

    final_gpu = get_gpu_memory_usage()
    final_sys = get_system_resources()

    avg_inference_time = sum(inference_times) / len(inference_times)
    max_inference_time = max(inference_times)
    min_inference_time = min(inference_times)

    avg_gpu_memory = sum(gpu_memory_samples) / len(gpu_memory_samples)
    max_gpu_memory = max(gpu_memory_samples)

    avg_cpu = sum(cpu_samples) / len(cpu_samples)
    avg_ram = sum(ram_samples) / len(ram_samples)
    max_ram = max(ram_samples)

    resource_stats = {
        "model_load_time_sec": load_time,
        "inference_times": {
            "average_sec": avg_inference_time,
            "min_sec": min_inference_time,
            "max_sec": max_inference_time,
            "total_sec": sum(inference_times),
        },
        "gpu_memory_mb": {
            "average_allocated": avg_gpu_memory,
            "max_allocated": max_gpu_memory,
            "peak_allocated": final_gpu['max_allocated_mb'],
            "final_reserved": final_gpu['reserved_mb'],
        },
        "cpu_usage": {
            "average_percent": avg_cpu,
        },
        "ram_mb": {
            "average": avg_ram,
            "max": max_ram,
            "final": final_sys['ram_mb'],
        },
    }

    print("\n===== SUMMARY METRICS =====")
    print(f"Total evaluated: {metrics['total']}")
    print(f"Exact category accuracy: {metrics['label_accuracy']*100:.2f}%")

    cm = metrics["anomaly_confusion_matrix"]
    print("\nAnomaly confusion matrix (positive = non-BENIGN):")
    print(f"TP={cm['TP']}  FP={cm['FP']}  TN={cm['TN']}  FN={cm['FN']}")

    am = metrics["anomaly_metrics"]
    print("\nAnomaly metrics:")
    print(f"Accuracy:            {am['accuracy']*100:.2f}%")
    print(f"Precision:           {am['precision']*100:.2f}%")
    print(f"Recall:              {am['recall']*100:.2f}%")
    print(f"F1:                  {am['f1']*100:.2f}%")
    print(f"False Positive Rate: {am['false_positive_rate']*100:.2f}%")

    print("\n===== RESOURCE USAGE =====")
    print(f"Model Load Time: {load_time:.2f}s")
    print(f"\nInference Time:")
    print(f"  Average: {avg_inference_time:.3f}s per sample")
    print(f"  Min:     {min_inference_time:.3f}s")
    print(f"  Max:     {max_inference_time:.3f}s")
    print(f"  Total:   {sum(inference_times):.2f}s")
    print(f"\nGPU Memory (VRAM):")
    print(f"  Average Allocated: {avg_gpu_memory:.2f} MB")
    print(f"  Max Allocated:     {max_gpu_memory:.2f} MB")
    print(f"  Peak Allocated:    {final_gpu['max_allocated_mb']:.2f} MB")
    print(f"  Final Reserved:    {final_gpu['reserved_mb']:.2f} MB")
    print(f"\nCPU Usage:")
    print(f"  Average: {avg_cpu:.2f}%")
    print(f"\nRAM Usage:")
    print(f"  Average: {avg_ram:.2f} MB")
    print(f"  Max:     {max_ram:.2f} MB")
    print(f"  Final:   {final_sys['ram_mb']:.2f} MB")

    out_path = 'Path'
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "metrics": metrics,
            "resource_usage": resource_stats,
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\nSaved detailed results to: {out_path}")

    print(f"\nFalse positive count: {cm['FP']}")
    print(f"False negative count: {cm['FN']}")
    print(f"True positives count: {cm['TP']}")
    print(f"True negatives count: {cm['TN']}")
    print(f"Total cases count: {metrics['total']}")

if __name__ == "__main__":
    main()
