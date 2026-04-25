import pandas as pd

new_dataset_path = "data/new_dataset/common_passwords.csv"
processed_dataset_path = "data/processed_dataset/cleaned_dataset.csv"

min_password_length = 4
max_password_length = 6

df = pd.read_csv(new_dataset_path)
df = df[['password']]

df = df[df['password'].str.len() >= min_password_length]
df = df[df['password'].str.len() <= max_password_length]

df = df[~df['password'].str.isdigit()]

df = df.drop_duplicates()
df.to_csv(processed_dataset_path, index = False)

print(f"Done. Cleaned dataset saved to {processed_dataset_path}")