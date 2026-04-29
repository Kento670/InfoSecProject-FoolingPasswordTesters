import pandas as pd

from config import GENERATED_PASSWORDS_DIR, MERGED_GENERATED_PATH

first_csv = GENERATED_PASSWORDS_DIR / "verified_passwords_v1.csv"
second_csv = GENERATED_PASSWORDS_DIR / "verified_passwords_v5.csv"


def read_password_csv(path):
    df = pd.read_csv(path)
    if "password" not in df.columns:
        df = pd.read_csv(path, header=None, names=["password"])
    return df[["password"]].dropna()


df_source = read_password_csv(first_csv)
df_dest = read_password_csv(second_csv)

combined = pd.concat([df_dest, df_source], ignore_index=True)
combined["password"] = combined["password"].astype(str).str.strip()
combined = combined[combined["password"].ne("")]
combined = combined.drop_duplicates().sample(frac=1, random_state=47205).reset_index(drop=True)

MERGED_GENERATED_PATH.parent.mkdir(parents=True, exist_ok=True)
combined.to_csv(MERGED_GENERATED_PATH, index=False)

print(f"New merged file created: {MERGED_GENERATED_PATH} ({len(combined)} unique passwords)")

