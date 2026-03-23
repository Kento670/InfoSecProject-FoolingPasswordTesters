# InfoSecProject-FoolingPasswordTesters


How to run:

Command: python clean_dataset.py
Success Message: Done. Cleaned dataset saved to data/processed_dataset/cleaned_dataset.csv

Command: python combine_passwords.py
Success Message:Done. Combined Passwords dataset saved to data/processed_dataset/combined_passwords.csv

Command: python combine_passwords.py
Success Message:Done. Combined Passwords dataset saved to data/processed_dataset/combined_passwords.csv

Command: python score_password.py
Success Message:Training dataset saved to data/training_dataset/training_dataset.csv

Command: python format_dataset.py
Success Message: Training JSONL file created and saved to data/training_dataset/training_dataset.jsonl

python train_model.py

Command: save_trained_model.py
Success Message: Done. Final Model saved to "models/final_model"

Command: python generate_passwords.py
Success Message: Done. Generated Password dataset saved to data/generated_passwords/passwords.csv

Command: python generate_passwords.py
Success Message: Done. Scored Generated Passwords, saved to data/generated_passwords/verified_passwords.csv

