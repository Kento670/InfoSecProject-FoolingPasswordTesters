import pandas as pd
import json

INPUT_PATH = "data/training_dataset/training_dataset.csv"
OUTPUT_PATH = "data/training_dataset/training_dataset.jsonl"

df = pd.read_csv(INPUT_PATH)

with open(OUTPUT_PATH, "w") as f:
    for pw in df['password']:
        record = {
            "prompt": "Generate a password that fools a strength meter:",
            "completion": pw
        }
        f.write(json.dumps(record) + "\n")
    
print("JSONL file created")