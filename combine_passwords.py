import pandas as pd
import random
from zxcvbn import zxcvbn

processed_dataset_path = "data/processed_dataset/cleaned_dataset.csv"
training_dataset_path = "data/processed_dataset/combined_passwords.csv"

patterns = [
    "123", "321", "111", "1234", "4321",
    "@1990", "@1991", "@1992", "@2000", "@2001", "@2002",
    "!2020", "!2021", "!2022",
    "#1", "#12", "#123",
    "_123", "_321", "_2001", "_2002",
]

df = pd.read_csv(processed_dataset_path)
passwords = df['password'].tolist()[:150]

modified_passwords = []

for pw in passwords:
    modified_passwords.append(pw)
    pattern = random.choice(patterns)
    modified_passwords.append(pw + pattern)

combined_passwords = []

for i in range(len(modified_passwords)):
    for j in range(i + 1, len(modified_passwords)):
        pass1 = modified_passwords[i]
        pass2 = modified_passwords[j]

        combined_passwords.append(pass1 + pass2)
        combined_passwords.append(pass2 + pass1)


df = pd.DataFrame(combined_passwords, columns=['password'])
df = df.drop_duplicates()

df.to_csv(training_dataset_path, index=False)

print(f"Done. Combined Passwords dataset saved to {training_dataset_path}")
