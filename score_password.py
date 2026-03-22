import pandas as pd
from zxcvbn import zxcvbn

CLEAN_DATASET_PATH = "data/processed_dataset/combined_passwords.csv"
TRAINING_DATASET_PATH = "data/training_dataset/training_dataset.csv"

ZXCVBN_LIMIT = 4

df = pd.read_csv(CLEAN_DATASET_PATH)

strong_passwords = []

for pw in df['password']:
    if zxcvbn(pw)['score'] >= ZXCVBN_LIMIT:
        strong_passwords.append(pw)

pd.DataFrame(strong_passwords, columns=['password']).to_csv(TRAINING_DATASET_PATH, index=False)\

print(f"Training dataset saved to {TRAINING_DATASET_PATH}")
