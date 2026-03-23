import pandas as pd
from zxcvbn import zxcvbn

processed_dataset_path = "data/processed_dataset/cleaned_dataset.csv"
training_dataset_path = "data/processed_dataset/combined_passwords.csv"

df = pd.read_csv(processed_dataset_path)
passwords = df['password'].tolist()[:50]

combined_passwords = []

for i in range(len(passwords)):
    if i % 10 == 0:
        print(f"Processing password {i}/{len(passwords)}")
    for j in range(i + 1, len(passwords)):
        pass1 = passwords[i]
        pass2 = passwords[j]

        combinedPass1 = pass1 + pass2
        combinedPass2 = pass2 + pass1

        combined_passwords.append(combinedPass1)
        combined_passwords.append(combinedPass2)


df = pd.DataFrame(combined_passwords, columns=['password'])

df = df.drop_duplicates()

df.to_csv(training_dataset_path, index=False)

print(f"Done. Combined Passwords dataset saved to {training_dataset_path}")
