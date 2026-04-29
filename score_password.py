import pandas as pd
from zxcvbn import zxcvbn

from config import MODIFIED_PASSWORDS_PATH, TRAINING_DATASET_PATH, ZXCVBN_TARGET_SCORE

df = pd.read_csv(MODIFIED_PASSWORDS_PATH).dropna(subset=["password"])

scored_passwords = [
    pw for pw in df['password']
    if zxcvbn(str(pw))['score'] >= ZXCVBN_TARGET_SCORE
]

df_scored = pd.DataFrame(scored_passwords, columns=['password'])

df_scored = df_scored.sample(frac=1, random_state=47205).reset_index(drop=True)

TRAINING_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
df_scored.to_csv(TRAINING_DATASET_PATH, index=False)

print(f"Training dataset saved to {TRAINING_DATASET_PATH} ({len(df_scored)} passwords scoring {ZXCVBN_TARGET_SCORE}+)")
