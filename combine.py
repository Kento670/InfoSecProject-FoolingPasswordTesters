import pandas as pd

first_csv = "data/generated_passwords/verified_passwords_v1.csv"    
second_csv = "data/generated_passwords/verified_passwords_v5.csv"
output_csv="data/generated_passwords/verified_passwords_1+5.csv"

df_source = pd.read_csv(first_csv, header=None, names=["password"])
df_dest = pd.read_csv(second_csv, header=None, names=["password"])

combined = pd.concat([df_dest, df_source], ignore_index=True)
combined = combined.drop_duplicates()

combined = combined.sample(frac=1).reset_index(drop=True)

combined.to_csv(output_csv, index=False, header=False)

print(f"New merged file created: {output_csv}")

