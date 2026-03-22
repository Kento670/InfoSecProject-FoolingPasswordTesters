import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType

MODEL_NAME = "Qwen/Qwen2-0.5B"
DATA_PATH = "data/training_dataset/training_dataset.jsonl"
OUTPUT_PATH = "models/trained_model"

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

dataset = load_dataset("json", data_files=DATA_PATH)["train"]

def tokenize(example):
    prompt = example["prompt"] + "\n"
    completion = example["completion"] + tokenizer.eos_token

    prompt_tokens = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    completion_tokens = tokenizer(completion, add_special_tokens=False)["input_ids"]

    input_ids = prompt_tokens + completion_tokens

    labels = [-100] * len(prompt_tokens) + completion_tokens

    pad_len = 512 - len(input_ids)
    input_ids = input_ids + [tokenizer.pad_token_id] * pad_len
    labels = labels + [-100] * pad_len
    attention_mask = [1] * (512 - pad_len) + [0] * pad_len

    return {
        "input_ids": input_ids[:512],
        "attention_mask": attention_mask[:512],
        "labels": labels[:512]
    }

dataset = dataset.map(tokenize)

lora_config = LoraConfig(
    r=4,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir=OUTPUT_PATH,
    per_device_train_batch_size=2,
    num_train_epochs=2,
    logging_steps=10,
    save_steps=50,
    dataloader_pin_memory=False,
    fp16=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()
