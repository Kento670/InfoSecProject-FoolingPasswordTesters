# InfoSec Project: Fooling Password Strength Testers

## Overview
This project explores the possiblity of attackers use machine learning to generate adversarial passwords, passwords that appear strong to password strength meters but are actually predictable or weak. The goal is to train a llm that can generate passwords that score high on zxcvbn but arre still vulnerable to targeted attacks and analyze the scoring algorithms for strength meters.

---

## Technologies Used
- Python 3.12
- Pandas 
- Hugging Face Transformers
- Hugging Face Datasets
- PEFT 
- LoRA 
- PyTorch
- zxcvbn

---

## Models Used

### Base Model
- **Qwen/Qwen2-0.5B**
  - Size: ~0.5 billion parameters

### Fine-Tuning Method
- **LoRA (Low-Rank Adaptation)**
  - Efficient fine-tuning without updating full model weights
  - Reduces memory and compute requirements

---

## Methods

### 1. Data Collection & Cleaning
- Started with a dataset of common passwords
- Cleaned and removed duplicates
- Filtered out invalid passwords

### 2. Adversarial Password Generation
- Combined existing weak passwords to create stronger-looking ones
- Examples:
  - `Password123!Login123!`
  - `Qwerty2024#Summer2024`

### 3. Dataset Formatting
- Converted data into JSONL format for training
- Instruction-style formatting used for fine-tuning

### 4. Model Training
- Fine-tuned Qwen model using:
  - LoRA configuration
  - Hugging Face `Trainer`
- Training performed locally (CPU/AMD GPU environment)
- Generated multiple checkpoints during training

### 5. Model Inference
- Loaded final trained model
- Generated passwords using prompts

### 6. Results
- Model successfully generated structured passwords
- Issues encountered:
  - Repetition of common patterns
  - Occasional non-password text generation

### 7. Future Work
- Improve dataset diversity
- Increase dataset size
- Refine prompt structure
- Evaluate generated passwords using `zxcvbn`

---

## How to Run

```bash
pip install torch transformers datasets peft pandas zxcvbn
```


| Step | Command | Success Message |
|------|---------|-----------------|
| 1. Clean dataset | `python clean_dataset.py` | `Done. Cleaned dataset saved to data/processed_dataset/cleaned_dataset.csv` |
| 2. Combine passwords | `python combine_passwords.py` | `Done. Combined Passwords dataset saved to data/processed_dataset/combined_passwords.csv` |
| 3. Score passwords | `python score_password.py` | `Training dataset saved to data/training_dataset/training_dataset.csv` |
| 4. Format dataset | `python format_dataset.py` | `Training JSONL file created and saved to data/training_dataset/training_dataset.jsonl` |
| 5. Train model | `python train_model.py` | *(see training logs)* |
| 6. Save model | `python save_trained_model.py` | `Done. Final Model saved to "models/final_model"` |
| 7. Generate passwords | `python generate_passwords.py` | `Done. Generated Password dataset saved to data/generated_passwords/passwords.csv` |
| 8. Score generated passwords | `python score_generated_passwords.py` | `Done. Scored Generated Passwords, saved to data/generated_passwords/verified_passwords.csv` |
