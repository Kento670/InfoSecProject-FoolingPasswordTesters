import pandas as pd
from zxcvbn import zxcvbn

processed_dataset_path = "data/processed_dataset/modified_passwords.csv"
training_dataset_path = "data/training_dataset/training_dataset.csv"

zxcvbn_score = 3

df = pd.read_csv(processed_dataset_path)

scored_passwords = [
    pw for pw in df['password']
    if zxcvbn(pw)['score'] >= zxcvbn_score
]

df_scored = pd.DataFrame(scored_passwords, columns=['password'])

df_scored = df_scored.sample(frac=1).reset_index(drop=True)

df_scored.to_csv(training_dataset_path, index=False)

print(f"Training dataset saved to {training_dataset_path}")
