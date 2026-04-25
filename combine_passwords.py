import pandas as pd
import random
from zxcvbn import zxcvbn

processed_dataset_path = "data/processed_dataset/cleaned_dataset.csv"
training_dataset_path = "data/processed_dataset/combined_passwords.csv"

phrases = ["summer", "winter", "fall", "spring", "test", "admin", "user"]
symbols = ["@", "!", "#", "_"]
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


df = pd.read_csv(processed_dataset_path)
passwords = df['password'].tolist()

modified_passwords = []

for pw in passwords:
    modified_passwords.append(pw)

    for _ in range(3):
        pattern = generate_pattern()
        modified_passwords.append(pw + pattern)
        modified_passwords.append(pattern + pw)



df = pd.DataFrame(modified_passwords, columns=['password'])
df = df.drop_duplicates()

df.to_csv(training_dataset_path, index=False)

print(f"Done. Combined Passwords dataset saved to {training_dataset_path}")
