import pandas as pd
import random

from config import CLEANED_PASSWORDS_PATH, MODIFIED_PASSWORDS_PATH

phrases = ["summer", "winter", "fall", "spring", "test", "admin", "user"]
symbols = ["@", "!", "#", "_",]
years = list(range(1990, 2025))

def generate_pattern():
    phrase = random.choice(phrases)
    symbol = random.choice(symbols)
    year = str(random.choice(years))

    formats = [
        f"{phrase}{symbol}{year}",
        f"{year}{symbol}{phrase}",
        f"{phrase}{year}{symbol}",
        f"{symbol}{year}{phrase}",
    ]

    return random.choice(formats)


random.seed(47205)

df = pd.read_csv(CLEANED_PASSWORDS_PATH).dropna(subset=["password"])
passwords = df['password'].tolist()

modified_passwords = []

for pw in passwords:
    modified_passwords.append(pw)

    for _ in range(1):
        pattern = generate_pattern()
        modified_passwords.append(pw + pattern)
        modified_passwords.append(pattern + pw)


df = pd.DataFrame(modified_passwords, columns=['password'])
df = df.drop_duplicates()

MODIFIED_PASSWORDS_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(MODIFIED_PASSWORDS_PATH, index=False)

print(f"Done. Modified password dataset saved to {MODIFIED_PASSWORDS_PATH} ({len(df)} rows)")
