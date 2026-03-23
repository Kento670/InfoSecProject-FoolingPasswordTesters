import pandas as pd
from zxcvbn import zxcvbn

generated_passwords_path = "data/generated_passwords/passwords.csv"
output_path = "data/generated_passwords/verified_passwords.csv"

ZXCVBN_LIMIT = 4

df = pd.read_csv(generated_passwords_path)

scored_passwords = []

for pw in df['password']:
    pw = str(pw).strip()

    if zxcvbn(pw)['score'] >= ZXCVBN_LIMIT:
        scored_passwords.append(pw)

result = pd.DataFrame(scored_passwords, columns=['password'])
result = result.drop_duplicates()
result.to_csv(output_path, index=False)

print(f"Done. Scored Generated Passwords, saved to {output_path}")