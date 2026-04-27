import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from zxcvbn import zxcvbn

base_model_name = "Qwen/Qwen2-0.5B"
final_model_path = "models/final_model/final_model_v4"
output_path = "data/generated_passwords/verified_passwords.csv"

base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, final_model_path)
tokenizer = AutoTokenizer.from_pretrained(final_model_path)

model.to("cpu")
model.eval()

def generate_password():
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

target = 10000
batch_size = 200
zxcvbn_score = 4

strong_passwords = set()

while len(strong_passwords) < target:
    print(f"Generating - Current password count: {len(strong_passwords)}")

    batch = [generate_password() for _ in range(batch_size)]

    for pw in batch:
        score = zxcvbn(pw)["score"]
        if score >= zxcvbn_score:
            strong_passwords.add(pw)

    df = pd.DataFrame(sorted(strong_passwords), columns=["password"])
    df.to_csv(output_path, index=False)

print(f"Done! Saved {len(strong_passwords)} strong passwords to {output_path}")
