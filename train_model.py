import argparse

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Qwen with LoRA.")
    parser.add_argument("--model-name", default="Qwen/Qwen2-0.5B")
    parser.add_argument("--dataset", default="data/training_dataset/training_dataset_v1.jsonl")
    parser.add_argument("--output", default="models/trained_model")
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--save-steps", type=int, default=100)
    args = parser.parse_args()

    model = AutoModelForCausalLM.from_pretrained(args.model_name)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dataset = load_dataset("json", data_files=args.dataset)["train"]

    def tokenize(example):
        text = f"{example['instruction']}\n{example['response']}"

        tokens = tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=256,
        )

        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    dataset = dataset.map(tokenize)

    lora_config = LoraConfig(
        r=4,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)

    training_args = TrainingArguments(
        output_dir=args.output,
        per_device_train_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        logging_steps=25,
        save_steps=args.save_steps,
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
    trainer.train()


if __name__ == "__main__":
    main()
