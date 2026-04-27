# InfoSec Project: Fooling Password Strength Testers

## Overview

This project explores adversarial machine learning against password strength meters. The goal is to generate passwords that receive high `zxcvbn` scores while still being predictable under a targeted attack model.

The submitted pipeline includes:

- a rule-based data preparation pipeline built from common passwords
- a LoRA fine-tuned Qwen/Qwen2-0.5B language model
- a generator that samples model outputs and keeps passwords with high `zxcvbn` scores
- a 10,000+ password generated dataset
- an attackability evaluation showing that many high-scoring outputs still contain common-password material

## Deliverables

| Requirement | Status | Evidence |
| --- | --- | --- |
| Script that generates passwords scoring high on strength meters | Complete for `zxcvbn` | `generate_passwords.py` filters generated outputs by `zxcvbn` score. |
| Trained ML model | Complete | LoRA adapter files are in `models/final_model/final_model_v4`; checkpoint files are in `models/trained_model/checkpoint-800`. |
| Dataset of 10,000+ generated adversarial passwords | Complete | `data/generated_passwords/verified_passwords_v1.csv` contains 10,094 generated passwords. |
| Evidence that generated passwords are weak | Added | `evaluate_attackability.py` writes `ATTACKABILITY_REPORT.md` and `data/generated_passwords/attackability_results.csv`. |

## Results Summary

The primary generated dataset is `data/generated_passwords/verified_passwords_v1.csv`.

- Generated passwords evaluated: 10,094
- Passwords with `zxcvbn` score 4: 10,094
- Passwords matched by the targeted attackability check: 9,102
- Targeted-match rate: 90.17%

The important adversarial result is that these passwords appear strong to `zxcvbn`, but most still contain common-password material that a targeted attacker can prioritize.

See `ATTACKABILITY_REPORT.md` for the generated report.

## Project Structure

```text
.
|-- clean_dataset.py
|-- modify_passwords.py
|-- score_password.py
|-- format_dataset.py
|-- train_model.py
|-- save_trained_model.py
|-- generate_passwords.py
|-- score_generated_passwords.py
|-- evaluate_attackability.py
|-- data/
|   |-- new_dataset/common_passwords.csv
|   |-- processed_dataset/
|   |-- training_dataset/
|   `-- generated_passwords/
`-- models/
    |-- trained_model/checkpoint-800/
    `-- final_model/final_model_v4/
```

## Setup

```bash
pip install -r requirements.txt
```

## Reproduce the Data Pipeline

```bash
python clean_dataset.py
python modify_passwords.py --output data/processed_dataset/modified_passwords.csv
python score_password.py --input data/processed_dataset/modified_passwords.csv --output data/training_dataset/training_dataset.csv --min-score 3
python format_dataset.py --input data/training_dataset/training_dataset.csv --output data/training_dataset/training_dataset.jsonl
```

## Train and Save the Model

The committed model artifacts are already present. To retrain:

```bash
python train_model.py --dataset data/training_dataset/training_dataset_v1.jsonl --output models/trained_model
python save_trained_model.py --checkpoint models/trained_model/checkpoint-800 --output models/final_model/final_model_v4
```

## Generate and Evaluate Passwords

```bash
python generate_passwords.py --adapter models/final_model/final_model_v4 --output data/generated_passwords/verified_passwords.csv --target 10000 --min-score 4
python score_generated_passwords.py --input data/generated_passwords/verified_passwords_v1.csv --output data/generated_passwords/scored_generated_passwords.csv
python evaluate_attackability.py --generated data/generated_passwords/verified_passwords_v1.csv --output data/generated_passwords/attackability_results.csv --report ATTACKABILITY_REPORT.md
```

## Method

1. Start from a common-password dataset.
2. Clean the dataset by removing duplicates, numeric-only passwords, and passwords outside the selected length range.
3. Create adversarial-looking variants by combining common passwords with season/admin/test/user phrases, symbols, and years.
4. Keep variants that score high enough on `zxcvbn` for training.
5. Fine-tune Qwen/Qwen2-0.5B with LoRA on instruction-response examples.
6. Generate candidate passwords from the trained adapter.
7. Keep generated passwords that score 4 on `zxcvbn`.
8. Evaluate whether generated passwords still match a compact targeted attack model.

## Limitations

This repository currently evaluates `zxcvbn`; it does not implement the Dropbox meter directly. The attackability check is a targeted rule-set analysis rather than a full hashcat or John the Ripper cracking benchmark. A stronger final version could add a real cracking experiment and compare multiple strength meters side by side.
