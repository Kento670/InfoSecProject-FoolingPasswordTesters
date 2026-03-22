import pandas as pd
from zxcvbn import zxcvbn

CLEAN_DATASET_PATH = "data/processed_dataset/cleaned_dataset.csv"
TRAINING_DATASET_PATH = "data/processed_dataset/combined_passwords.csv"

df = pd.read_csv(CLEAN_DATASET_PATH)
passwords = df['password'].tolist()[:50]

adversarial = []

for i in range(len(passwords)):
    if i % 10 == 0:
        print(f"Processing password {i}/{len(passwords)}")
    for j in range(i + 1, len(passwords)):
        pass1 = passwords[i]
        pass2 = passwords[j]

        combinedPass1 = pass1 + pass2
        combinedPass2 = pass2 + pass1

        adversarial.append(combinedPass1)
        adversarial.append(combinedPass2)


df = pd.DataFrame(adversarial, columns=['password'])

df = df.drop_duplicates()

df.to_csv(TRAINING_DATASET_PATH, index=False)

print("Adversarial dataset created")
