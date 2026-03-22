import pandas as pd
from zxcvbn import zxcvbn

GENERATED_PASSWORDS_PATH = "data/generated_passwords/passwords.csv"
OUTPUT_PATH = "data/generated_passwords/verified_passwords.csv"

ZXCVBN_LIMIT = 4

df = pd.read_csv(GENERATED_PASSWORDS_PATH)

strong_passwords = []

for pw in df['password']:
    pw = str(pw).strip()

    if len(pw) > 16:
        continue

    if ' ' in pw:
        continue

    if ':' in pw:
        continue

    if zxcvbn(pw)['score'] >= ZXCVBN_LIMIT:
        strong_passwords.append(pw)

result = pd.DataFrame(strong_passwords, columns=['password'])
result = result.drop_duplicates()
result.to_csv(OUTPUT_PATH, index=False)

print("done")