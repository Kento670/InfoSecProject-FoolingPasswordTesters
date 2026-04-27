import argparse

import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from zxcvbn import zxcvbn


def generate_password(model, tokenizer):
    instructions = "Generate a password that fools a strength meter:\n"
    inputs = tokenizer(instructions, return_tensors="pt")
    instructions_len = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=30,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
        )

    generated = outputs[0][instructions_len:]
    password = tokenizer.decode(generated, skip_special_tokens=True)
    return password.replace("\n", "").strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate zxcvbn-high passwords from the fine-tuned LoRA model."
    )
    parser.add_argument("--base-model", default="Qwen/Qwen2-0.5B")
    parser.add_argument("--adapter", default="models/final_model/final_model_v4")
    parser.add_argument("--output", default="data/generated_passwords/verified_passwords.csv")
    parser.add_argument("--target", type=int, default=10000)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--min-score", type=int, default=4)
    args = parser.parse_args()

    base_model = AutoModelForCausalLM.from_pretrained(args.base_model)
    model = PeftModel.from_pretrained(base_model, args.adapter)
    tokenizer = AutoTokenizer.from_pretrained(args.adapter)

    model.to("cpu")
    model.eval()

    strong_passwords = set()

    while len(strong_passwords) < args.target:
        print(f"Generating - Current password count: {len(strong_passwords)}")

        batch = [generate_password(model, tokenizer) for _ in range(args.batch_size)]

        for password in batch:
            score = zxcvbn(password)["score"]
            if score >= args.min_score:
                strong_passwords.add(password)

        df = pd.DataFrame(sorted(strong_passwords), columns=["password"])
        df.to_csv(args.output, index=False)

    print(f"Done! Saved {len(strong_passwords)} strong passwords to {args.output}")


if __name__ == "__main__":
    main()
