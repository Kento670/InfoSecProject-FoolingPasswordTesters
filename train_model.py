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
    text = example["prompt"] + "\n" + example["completion"]
    tokens = tokenizer(text, truncation=True, padding="max_length", max_length=512)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

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
    per_device_train_batch_size=1,
    num_train_epochs=2,
    logging_steps=25,
    save_steps=100,
    dataloader_pin_memory=False,
    fp16=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()
