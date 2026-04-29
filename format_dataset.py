import pandas as pd
import json

from config import TRAINING_DATASET_PATH, TRAINING_JSONL_PATH


df = pd.read_csv(TRAINING_DATASET_PATH).dropna(subset=["password"])
TRAINING_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(TRAINING_JSONL_PATH, "w", encoding="utf-8") as f:
    for pw in df['password']:
        record = {
            "instruction": "Generate a password that fools a strength meter:",
            "response": pw
        }
        f.write(json.dumps(record) + "\n")
    
print(f"Training JSONL file created with {len(df)} records and saved to {TRAINING_JSONL_PATH}")
