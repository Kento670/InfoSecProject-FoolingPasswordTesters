# Adversarial ML Against Password Strength Meters

This project explores whether machine learning can generate passwords that receive high scores from password strength meters while still following predictable, attackable patterns.

The core experiment fine-tunes a small language model on weak-password transformations that look complex to `zxcvbn`: common words, seasons, years, symbols, capitalization, and concatenated phrases. The generated passwords are then filtered by `zxcvbn` score to create an adversarial dataset.

## Deliverables

- Script pipeline for generating high-scoring adversarial passwords
- Fine-tuned Qwen2-0.5B LoRA adapter
- 10,000+ generated adversarial passwords
- Scoring and summary scripts for presentation-ready results

## Current Results

- `verified_passwords_v1.csv`: 10,095 generated passwords
- `verified_passwords_v5.csv`: 10,042 generated passwords
- `verified_passwords_1+5.csv`: merged adversarial set with about 19,500 unique passwords

These outputs are designed to score well on `zxcvbn`, but many still contain predictable structures such as seasons, years, roles, common words, and simple symbol insertion.

## Project Structure

```text
.
├── clean_dataset.py              # Clean raw common-password data
├── modify_passwords.py           # Create weak but complex-looking transformations
├── score_password.py             # Keep training candidates that zxcvbn scores highly
├── format_dataset.py             # Convert CSV training data to JSONL
├── train_model.py                # Fine-tune Qwen2-0.5B with LoRA
├── save_trained_model.py         # Save a selected checkpoint as the final adapter
├── generate_passwords.py         # Generate and filter adversarial passwords
├── score_generated_passwords.py  # Score generated outputs and keep high-score rows
├── summarize_results.py          # Print quick result statistics for slides/demo
├── analyze_patterns.py           # Show why high-scoring outputs are still predictable
├── rule_attack_simulation.py     # Test whether simple targeted rules recover outputs
├── baseline_comparison.py        # Compare weak, generated, and random password sets
├── app.py                        # Flask dashboard for the project demo
├── templates/
├── static/
├── config.py                     # Shared paths and constants
├── requirements.txt
├── data/
└── models/
```

## Setup

```bash
pip install -r requirements.txt
```

For CPU-only machines, model training and generation may be slow. The result-summary scripts can still run quickly on the generated CSV files.

## Flask Dashboard

Run the local web app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The dashboard shows the generated dataset summary, predictable pattern analysis, sample adversarial passwords, a zxcvbn password checker, and a CSV download link.

The app is intentionally simple: it is a usable password lab, not a report page. It includes an instant demo generator, a targeted attack test, and a baseline comparison table.

## Reproduce the Pipeline

```bash
python clean_dataset.py
python modify_passwords.py
python score_password.py
python format_dataset.py
python train_model.py
python save_trained_model.py
python generate_passwords.py
python score_generated_passwords.py
```

## Short Training and Generation Demo

For a 15-minute presentation, do not retrain the full dataset live unless required. Use a small training subset and generate a small sample:

```bash
python train_model.py --max-records 200 --epochs 1 --save-steps 50 --logging-steps 10 --output-dir models/trained_model_demo
python save_trained_model.py --checkpoint models/trained_model_demo --output-dir models/final_model/demo_model
python generate_passwords.py --target 25 --batch-size 10 --model-dir models/final_model/demo_model --output data/generated_passwords/demo_generated_passwords.csv
python score_generated_passwords.py --input data/generated_passwords/demo_generated_passwords.csv --output data/generated_passwords/demo_verified_passwords.csv
```

This proves the code path works without waiting for a full 10,000-password generation run.

For the full run, use:

```bash
python train_model.py
python save_trained_model.py
python generate_passwords.py --target 10000
```

## Merge and Summarize Results

Merge the two strongest generated sets:

```bash
python combine.py
```

Print presentation-ready statistics:

```bash
python summarize_results.py
```

Show predictable pattern counts:

```bash
python analyze_patterns.py
```

Run the rule-based attacker simulation:

```bash
python rule_attack_simulation.py --max-roots 100
```

Compare generated outputs against common weak passwords and random passwords:

```bash
python baseline_comparison.py --sample-size 150
```

Score a specific generated CSV:

```bash
python score_generated_passwords.py --input data/generated_passwords/verified_passwords_v5.csv --output data/generated_passwords/verified_passwords_v5_scored.csv
```

## Method Summary

1. Start with common passwords.
2. Clean the dataset by removing duplicates, numeric-only strings, and out-of-range lengths.
3. Apply adversarial transformations:
   - append or prepend seasons, roles, and years
   - add simple symbols
   - preserve recognizable weak roots
4. Filter candidates that score at least `4` on `zxcvbn`.
5. Fine-tune `Qwen/Qwen2-0.5B` using LoRA.
6. Generate new passwords and keep those that still score highly.
7. Analyze why the meter accepts them despite obvious predictable structure.

## Key Takeaway

Password meters can reward surface complexity even when the password is built from common, guessable components. The adversarial examples show that a high score is not the same thing as resistance to targeted guessing.
