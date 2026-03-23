import pandas as pd
from zxcvbn import zxcvbn

processed_dataset_path = "data/processed_dataset/combined_passwords.csv"
training_dataset_path = "data/training_dataset/training_dataset.csv"

zxcvbn_score = 4

df = pd.read_csv(processed_dataset_path)

scored_passwords = []

for pw in df['password']:
    if zxcvbn(pw)['score'] >= zxcvbn_score:
        scored_passwords.append(pw)

pd.DataFrame(scored_passwords, columns=['password']).to_csv(training_dataset_path, index=False)\

print(f"Training dataset saved to {training_dataset_path}")
