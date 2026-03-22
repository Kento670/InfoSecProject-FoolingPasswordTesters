import torch

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATA_PATH = "data/training_dataset/training_dataset.jsonl"
OUTPUT_PATH = "models/password_model"

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
dataset = load_dataset("json", data_files=DATA_PATH)["train"]

def tokenize(example):
    text = example["prompt"] + " " + example["completion"]
    return tokenizer(text, truncation=True, padding="max_length")

dataset = dataset.map(tokenize)

lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir=OUTPUT_PATH,
    per_device_train_batch_size=1,
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
