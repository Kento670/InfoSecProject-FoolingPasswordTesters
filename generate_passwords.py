import torch 
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model_name = "Qwen/Qwen2-0.5B"
final_model_path = "models/final_model"
output_path = "data/generated_passwords/passwords.csv"

base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, final_model_path)

tokenizer = AutoTokenizer.from_pretrained(final_model_path)


def generate_password():
    instructions = "Generate a password that fools a strength meter:\n"  
    inputs = tokenizer(instructions, return_tensors="pt")
    instructions_len = inputs["input_ids"].shape[1]

    outputs = model.generate(
        **inputs,
        max_new_tokens=30,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        do_sample=True,
    )

    generated = outputs[0][instructions_len:] 
    password = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return password

num_passwords = 10
generated = [generate_password() for i in range(num_passwords)]

df = pd.DataFrame(generated, columns=["password"])
df.to_csv(output_path, index=False)

print(f"Done. Generated Password dataset saved to {output_path}")

