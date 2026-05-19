from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
import json

MODEL_ID = "meta-llama/Llama-3.2-3B"

cleaned = []
with open("PATH", "rb") as f:
    for line in f:
        decoded = line.decode("utf-8", errors="ignore")
        try:
            cleaned.append(json.loads(decoded))
        except json.JSONDecodeError:
            continue

cleaned_path = "PATH"
with open(cleaned_path, "w", encoding="utf-8") as f:
    for item in cleaned:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

dataset = load_dataset("json", data_files=cleaned_path)

dataset = dataset["train"].train_test_split(test_size=0.1, seed=42)
print(f"Train: {len(dataset['train'])}, Val: {len(dataset['test'])}")

def format_example(example):
    prompt = (
        "### Instruction:\n"
        f"{example['instruction']}\n\n"
        "### Input:\n"
        f"{example['input']}\n\n"
        "### Response:\n"
        f"{example['output']}"
    )
    return {"text": prompt}

dataset["train"] = dataset["train"].map(format_example)
dataset["test"] = dataset["test"].map(format_example)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

def tokenize(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

dataset["train"] = dataset["train"].map(tokenize, remove_columns=dataset["train"].column_names)
dataset["test"] = dataset["test"].map(tokenize, remove_columns=dataset["test"].column_names)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    load_in_4bit=True,
    device_map="auto"
)

lora = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora)

args = TrainingArguments(
    output_dir="../output",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"]
)

trainer.train()