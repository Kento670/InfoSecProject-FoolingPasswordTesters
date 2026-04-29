import argparse

import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from zxcvbn import zxcvbn

from config import BASE_MODEL_NAME, DEFAULT_GENERATED_PATH, FINAL_MODEL_DIR, ZXCVBN_TARGET_SCORE

def clean_password(candidate):
    password = candidate.replace("\n", "").replace("\r", "").strip()
    password = password.split()[0] if password else ""
    password = password.strip('"').strip("'").strip()

    if not 8 <= len(password) <= 64:
        return ""
    if "," in password:
        return ""
    return password


def main():
    parser = argparse.ArgumentParser(description="Generate zxcvbn high-scoring adversarial passwords.")
    parser.add_argument("--target", type=int, default=10000, help="Number of verified passwords to generate.")
    parser.add_argument("--batch-size", type=int, default=200, help="Candidates to generate per loop.")
    parser.add_argument("--output", default=str(DEFAULT_GENERATED_PATH), help="Output CSV path.")
    parser.add_argument("--model-dir", default=str(FINAL_MODEL_DIR), help="Fine-tuned LoRA adapter directory.")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"], help="Generation device.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature.")
    parser.add_argument("--top-p", type=float, default=0.95, help="Nucleus sampling top-p value.")
    args = parser.parse_args()

    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_NAME)
    model = PeftModel.from_pretrained(base_model, args.model_dir)
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("CUDA requested but not available. Falling back to CPU.")
        device = "cpu"

    model.to(device)
    model.eval()

    def generate_password():
        instructions = "Generate a password that fools a strength meter:\n"
        inputs = tokenizer(instructions, return_tensors="pt").to(device)
        instructions_len = inputs["input_ids"].shape[1]

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=30,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                do_sample=True,
                temperature=args.temperature,
                top_p=args.top_p,
            )

        generated = outputs[0][instructions_len:]
        password = tokenizer.decode(generated, skip_special_tokens=True)
        return clean_password(password)

    output_path = pd.io.common.stringify_path(args.output)
    strong_passwords = set()

    while len(strong_passwords) < args.target:
        print(f"Generating - Current password count: {len(strong_passwords)}")

        batch = [generate_password() for _ in range(args.batch_size)]

        for pw in batch:
            if not pw:
                continue

            score = zxcvbn(pw)["score"]
            if score >= ZXCVBN_TARGET_SCORE:
                strong_passwords.add(pw)

        df = pd.DataFrame(sorted(strong_passwords), columns=["password"])
        pd.io.common.check_parent_directory(output_path)
        df.to_csv(output_path, index=False)

    print(f"Done! Saved {len(strong_passwords)} strong passwords to {output_path}")


if __name__ == "__main__":
    main()
