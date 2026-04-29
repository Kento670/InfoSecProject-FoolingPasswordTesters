import argparse

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

from config import BASE_MODEL_NAME, TRAINED_MODEL_DIR, TRAINING_DATASET_DIR, TRAINING_JSONL_PATH


def default_training_jsonl():
    if TRAINING_JSONL_PATH.exists():
        return TRAINING_JSONL_PATH

    versioned_path = TRAINING_DATASET_DIR / "training_dataset_v5.jsonl"
    if versioned_path.exists():
        return versioned_path

    return TRAINING_JSONL_PATH


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Qwen2-0.5B with LoRA on adversarial passwords.")
    parser.add_argument("--dataset", default=str(default_training_jsonl()), help="JSONL training dataset path.")
    parser.add_argument("--output-dir", default=str(TRAINED_MODEL_DIR), help="Directory for training checkpoints.")
    parser.add_argument("--epochs", type=float, default=1, help="Number of training epochs.")
    parser.add_argument("--batch-size", type=int, default=1, help="Per-device training batch size.")
    parser.add_argument("--max-records", type=int, default=None, help="Limit training rows for a faster demo run.")
    parser.add_argument("--max-length", type=int, default=128, help="Tokenizer max length.")
    parser.add_argument("--save-steps", type=int, default=100, help="Checkpoint save interval.")
    parser.add_argument("--logging-steps", type=int, default=25, help="Logging interval.")
    args = parser.parse_args()

    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dataset = load_dataset("json", data_files=args.dataset)["train"]
    if args.max_records:
        dataset = dataset.select(range(min(args.max_records, len(dataset))))

    dataset = dataset.train_test_split(test_size=0.1, seed=47205)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]

    def tokenize(example):
        text = f"{example['instruction']}\n{example['response']}"

        tokens = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=args.max_length
        )

        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    train_dataset = train_dataset.map(tokenize)
    eval_dataset = eval_dataset.map(tokenize)

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
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        eval_strategy="steps",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
    )

    trainer.train()
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print(f"Done. Trained LoRA adapter saved to {args.output_dir}")


if __name__ == "__main__":
    main()
