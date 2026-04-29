import pandas as pd

from config import CLEANED_PASSWORDS_PATH, RAW_PASSWORDS_PATH

min_password_length = 3
max_password_length = 9

df = pd.read_csv(RAW_PASSWORDS_PATH)
df = df[['password']]
df = df.dropna(subset=['password'])
df['password'] = df['password'].astype(str)

df = df[df['password'].str.len() >= min_password_length]
df = df[df['password'].str.len() <= max_password_length]

df = df[~df['password'].str.isdigit()]

df = df.drop_duplicates()
CLEANED_PASSWORDS_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(CLEANED_PASSWORDS_PATH, index=False)

print(f"Done. Cleaned {len(df)} passwords and saved to {CLEANED_PASSWORDS_PATH}")
