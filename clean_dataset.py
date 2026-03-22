import pandas as pd

RAW_DATASET_PATH = "data/new_dataset/common_passwords.csv"
CLEAN_DATASET_PATH = "data/processed_dataset/cleaned_dataset.csv"
MIN_PASSWORD_LENGTH = 7

df = pd.read_csv(RAW_DATASET_PATH)
df = df[['password']]
df = df[df['password'].str.len() >= MIN_PASSWORD_LENGTH]
df = df.drop_duplicates()
df.to_csv(CLEAN_DATASET_PATH, index = False)

print("done")