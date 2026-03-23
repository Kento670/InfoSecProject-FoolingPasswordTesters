import pandas as pd
import json

input_path = "data/training_dataset/training_dataset.csv"
output_path = "data/training_dataset/training_dataset.jsonl"

df = pd.read_csv(input_path)
with open(output_path, "w") as f:
    for pw in df['password']:
        record = {
            "prompt": "Generate a password that fools a strength meter:",
            "completion": pw
        }
        f.write(json.dumps(record) + "\n")
    
print("JSONL file created")
print(f"Training JSONL file created and saved to {output_path}")