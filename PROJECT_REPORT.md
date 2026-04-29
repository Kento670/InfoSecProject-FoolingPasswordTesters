# Project Report: Adversarial ML Against Password Strength Meters

## 1. Project Goal

This project studies whether machine learning can generate passwords that appear strong to password strength meters while still being predictable enough for an attacker to guess with targeted rules.

The main research question is:

> Can attackers use ML to generate passwords that fool strength meters while remaining easily crackable?

The project focuses on `zxcvbn`, a widely used password strength estimator. The generated passwords are considered adversarial because they receive high meter scores, but many are built from obvious patterns such as seasons, years, symbols, roles, and common words.

Example adversarial passwords from the project:

```text
@2021userfall
admin1997!spring!
#2015springfalluser
_1995winterfall
#2019springuser
```

These passwords look complex because they are long and contain numbers, words, and symbols. However, they are still predictable because they follow repeatable templates.

## 2. Project Deliverables

The assignment required three main deliverables.

| Requirement | How this project satisfies it |
|---|---|
| Script that generates passwords scoring high on strength meters but are actually weak | `generate_passwords.py` generates candidate passwords and filters them using `zxcvbn` score `>= 4`. |
| Trained ML model, such as a GAN or fine-tuned LLM | The project fine-tunes `Qwen/Qwen2-0.5B` using LoRA adapters. The final adapter is saved under `models/final_model/final_model_v5`. |
| Dataset of 10,000+ generated adversarial passwords | The merged generated dataset has `19,574` unique passwords in `data/generated_passwords/verified_passwords_1+5.csv`. |

## 3. High-Level Pipeline

The project works in this order:

1. Start with a dataset of common passwords.
2. Clean the raw password list.
3. Modify weak passwords so they look stronger.
4. Score modified passwords with `zxcvbn`.
5. Keep only passwords that score highly.
6. Format the training data as JSONL.
7. Fine-tune a language model with LoRA.
8. Use the fine-tuned model to generate new passwords.
9. Filter generated passwords with `zxcvbn`.
10. Merge and summarize the generated adversarial dataset.

In short:

```text
common passwords
    -> cleaned weak passwords
    -> modified complex-looking passwords
    -> zxcvbn high-score training data
    -> fine-tuned LLM
    -> generated adversarial passwords
    -> verified 10,000+ password dataset
```

## 4. Important Files

| File | Purpose |
|---|---|
| `config.py` | Stores shared file paths, model names, and the target `zxcvbn` score. |
| `clean_dataset.py` | Cleans the raw common-password dataset. |
| `modify_passwords.py` | Creates weak but complex-looking password variants. |
| `score_password.py` | Filters modified passwords that score highly on `zxcvbn`. |
| `format_dataset.py` | Converts the scored CSV into JSONL training format. |
| `train_model.py` | Fine-tunes the base Qwen model using LoRA. |
| `save_trained_model.py` | Saves a selected training checkpoint as the final model adapter. |
| `generate_passwords.py` | Uses the fine-tuned model to generate high-scoring passwords. |
| `score_generated_passwords.py` | Scores generated passwords and saves the verified high-score subset. |
| `combine.py` | Merges generated password datasets into one larger file. |
| `summarize_results.py` | Prints presentation-ready statistics and examples. |
| `analyze_patterns.py` | Measures predictable structures such as years, seasons, symbols, and account words. |
| `rule_attack_simulation.py` | Simulates a targeted attacker using simple password-generation rules. |
| `baseline_comparison.py` | Compares common weak passwords, generated adversarial passwords, and random passwords. |
| `app.py` | Runs the Flask dashboard for a visual project demo. |

## 5. Configuration: `config.py`

`config.py` centralizes the important constants used across the project.

It defines:

```python
BASE_MODEL_NAME = "Qwen/Qwen2-0.5B"
ZXCVBN_TARGET_SCORE = 4
```

It also defines paths such as:

```python
RAW_PASSWORDS_PATH
CLEANED_PASSWORDS_PATH
MODIFIED_PASSWORDS_PATH
TRAINING_DATASET_PATH
TRAINING_JSONL_PATH
FINAL_MODEL_DIR
DEFAULT_GENERATED_PATH
MERGED_GENERATED_PATH
```

This makes the code easier to maintain because scripts do not each need their own hard-coded file paths.

Why this matters:

- It reduces mistakes from inconsistent filenames.
- It makes the pipeline easier to explain.
- It lets the whole project use the same model name, dataset paths, and target score.

## 6. Cleaning the Dataset: `clean_dataset.py`

This script starts with the raw common-password file:

```text
data/new_dataset/common_passwords.csv
```

It keeps only the `password` column, removes missing values, and converts passwords to strings.

Then it filters passwords by length:

```python
min_password_length = 3
max_password_length = 9
```

This means the base passwords are intentionally short and weak. The project starts from weak passwords because the goal is to create passwords that are still guessable even after transformations.

It also removes numeric-only passwords:

```python
df = df[~df['password'].str.isdigit()]
```

Finally, it removes duplicates and saves:

```text
data/processed_dataset/cleaned_dataset.csv
```

What this script proves:

- The seed data is based on weak/common passwords.
- The model is not trained from random secure passwords.
- The adversarial examples are built from guessable roots.

## 7. Creating Weak but Complex-Looking Passwords: `modify_passwords.py`

This is one of the most important scripts in the project.

It takes cleaned weak passwords and adds predictable patterns to them. These patterns make the passwords look stronger to a meter but not necessarily stronger against a targeted attacker.

The script uses phrases such as:

```python
phrases = ["summer", "winter", "fall", "spring", "test", "admin", "user"]
```

It uses symbols such as:

```python
symbols = ["@", "!", "#", "_"]
```

It uses years:

```python
years = list(range(1990, 2025))
```

The function `generate_pattern()` creates patterns like:

```text
summer@2021
2021@summer
summer2021@
@2021summer
```

Then, for each weak password, the script creates variants by appending or prepending the generated pattern:

```python
modified_passwords.append(pw + pattern)
modified_passwords.append(pattern + pw)
```

Example:

If the weak password is:

```text
dragon
```

The transformed passwords might be:

```text
dragonwinter!2018
winter!2018dragon
```

Why this fools meters:

- The passwords become longer.
- They include numbers.
- They include symbols.
- They include multiple words.

Why they are still weak:

- They use common words.
- They use common seasons.
- They use common years.
- They use simple templates an attacker could reproduce.

The output is:

```text
data/processed_dataset/modified_passwords.csv
```

## 8. Scoring Training Passwords: `score_password.py`

This script reads:

```text
data/processed_dataset/modified_passwords.csv
```

Then it scores every password with:

```python
zxcvbn(pw)['score']
```

`zxcvbn` scores passwords from `0` to `4`:

| Score | Meaning |
|---|---|
| 0 | Very weak |
| 1 | Weak |
| 2 | Fair |
| 3 | Good |
| 4 | Strong |

The project keeps passwords with:

```python
score >= 4
```

That means the training dataset contains passwords that `zxcvbn` believes are strong.

The output is:

```text
data/training_dataset/training_dataset.csv
```

Why this matters:

The model learns to imitate passwords that already fool the strength meter.

## 9. Formatting the Dataset: `format_dataset.py`

The model training code expects JSONL data.

JSONL means each line is a separate JSON object.

The script converts each password into an instruction-response example:

```json
{"instruction": "Generate a password that fools a strength meter:", "response": "examplePassword"}
```

This teaches the language model:

```text
When given this instruction, output a password like the training examples.
```

The output is:

```text
data/training_dataset/training_dataset.jsonl
```

## 10. Model Training: `train_model.py`

This script fine-tunes:

```text
Qwen/Qwen2-0.5B
```

Qwen2-0.5B is a small language model with about 0.5 billion parameters.

The project uses Hugging Face Transformers:

```python
AutoModelForCausalLM
AutoTokenizer
Trainer
TrainingArguments
```

The training data is loaded from:

```text
data/training_dataset/training_dataset.jsonl
```

The dataset is split into:

```python
train_dataset
eval_dataset
```

The model is trained to predict the full text:

```text
Generate a password that fools a strength meter:
password_here
```

### LoRA Fine-Tuning

The script uses LoRA:

```python
LoraConfig(
    r=4,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
```

LoRA stands for Low-Rank Adaptation.

Instead of retraining the entire model, LoRA trains small adapter weights. This is useful because:

- It requires less memory.
- It is faster than full fine-tuning.
- It can work on smaller hardware.
- It keeps the base model mostly unchanged.

The trained checkpoints are saved under:

```text
models/trained_model
```

## 11. Saving the Final Model: `save_trained_model.py`

During training, checkpoints are created. A checkpoint is a saved version of the model at a certain training step.

This script loads a checkpoint:

```python
checkpoint_path = TRAINED_MODEL_DIR / "checkpoint-700"
```

Then it saves the final LoRA adapter to:

```text
models/final_model/final_model_v5
```

This final folder is what `generate_passwords.py` uses.

Important detail:

The final model is not a completely new full model. It is a LoRA adapter that works with the base Qwen model.

## 12. Generating Passwords: `generate_passwords.py`

This script loads:

1. The base model:

```text
Qwen/Qwen2-0.5B
```

2. The fine-tuned LoRA adapter:

```text
models/final_model/final_model_v5
```

It uses this prompt:

```text
Generate a password that fools a strength meter:
```

Then the model generates a candidate password.

The generation uses sampling:

```python
do_sample=True
temperature=0.7
top_p=0.95
```

What these mean:

| Setting | Meaning |
|---|---|
| `do_sample=True` | The model samples outputs instead of always choosing the same next token. |
| `temperature=0.7` | Controls randomness. Lower is more predictable, higher is more random. |
| `top_p=0.95` | Uses nucleus sampling, choosing from likely tokens that make up 95% probability mass. |

After generation, the script cleans the output:

- removes newlines
- strips quotes
- rejects empty outputs
- rejects outputs that are too short or too long
- rejects outputs containing commas

Then it scores each generated password with `zxcvbn`.

Only passwords with:

```python
score >= 4
```

are added to the final set.

The script keeps generating until it reaches:

```python
target = 10000
```

The default output is:

```text
data/generated_passwords/verified_passwords_v5.csv
```

## 13. Scoring Generated Passwords: `score_generated_passwords.py`

This script is used after generation.

It reads a generated password CSV and computes:

- password
- `zxcvbn_score`
- estimated guesses
- offline cracking estimate
- feedback warning

It keeps only passwords scoring at least `4`.

This script is useful because it gives evidence that the generated passwords really score highly according to `zxcvbn`.

Example command:

```powershell
python score_generated_passwords.py --input data/generated_passwords/verified_passwords_v5.csv --output data/generated_passwords/verified_passwords_v5_scored.csv
```

## 14. Combining Generated Datasets: `combine.py`

The project has multiple generated password files from different versions.

The two strongest are:

```text
verified_passwords_v1.csv
verified_passwords_v5.csv
```

`combine.py` merges these two files, removes duplicates, shuffles them, and saves:

```text
data/generated_passwords/verified_passwords_1+5.csv
```

The merged file contains:

```text
19,574 unique passwords
```

This satisfies the assignment requirement of 10,000+ generated adversarial passwords.

## 15. Summarizing Results: `summarize_results.py`

This script prints a quick summary for presentations.

Run:

```powershell
python summarize_results.py
```

Expected output:

```text
Generated password summary
==========================
Unique passwords: 19,574
Scoring 4/4 on zxcvbn: 19,574 (100.0%)
Average length: 16.5
```

To print more examples:

```powershell
python summarize_results.py --examples 15
```

To force a full `zxcvbn` rescore:

```powershell
python summarize_results.py --rescore
```

The default mode is fast because the merged file is already a verified high-score dataset. The `--rescore` option is slower but useful if someone wants to see the scores recomputed live.

## 16. How `zxcvbn` Works

`zxcvbn` does not simply count symbols, uppercase letters, lowercase letters, and numbers. It estimates password strength by looking for patterns.

It checks for things like:

- dictionary words
- common passwords
- names
- repeated characters
- keyboard patterns
- dates
- sequences
- leetspeak substitutions
- multiple matched patterns inside one password

Then it estimates how many guesses an attacker might need.

Finally, it converts that guess estimate into a score from `0` to `4`.

The weakness exploited in this project is that a password can contain recognizable words and years but still get a high score if it is long enough and combines several components.

## 16.1. Pattern Analysis: `analyze_patterns.py`

This script strengthens the "actually weak" argument.

It reads the merged generated dataset and counts predictable features:

- year-like values, such as `1997` or `2021`
- seasons, such as `spring`, `summer`, `fall`, and `winter`
- account-related words, such as `admin`, `user`, `test`, and `login`
- symbols
- passwords that start with a symbol
- templates combining both a season and year
- templates combining both an account word and year

Run it with:

```powershell
python analyze_patterns.py
```

This gives you a presentation slide that directly supports the claim that the passwords are high-scoring but predictable.

## 16.2. Rule-Based Attacker Simulation

`rule_attack_simulation.py` tests the "actually weak" claim more directly.

It builds guesses using targeted rules such as:

```text
symbol + year + word + season
word + year + symbol + season
season + year + symbol + word
word + season + year + symbol
```

With 100 common roots, the attacker simulation generated 488,448 guesses and recovered 2,808 passwords from the generated dataset, which is 14.3% of the 19,574-password merged set.

This matters because the attack is not random brute force. It is a targeted guess generator based on the same predictable structures that appear in the model outputs.

Run it with:

```powershell
python rule_attack_simulation.py --max-roots 100
```

## 16.3. Baseline Comparison

`baseline_comparison.py` compares three datasets:

- common weak passwords
- generated adversarial passwords
- random passwords with similar length

The useful result is that random passwords and generated adversarial passwords both score highly on zxcvbn, but only the generated adversarial passwords contain large amounts of season/year structure.

Run it with:

```powershell
python baseline_comparison.py --sample-size 150
```

## 17. Why These Passwords Fool the Meter

The generated passwords often have:

- long length
- symbols
- numbers
- multiple words
- year-like values
- mixed structure

For example:

```text
admin1997!spring!
```

This password has:

- a role word: `admin`
- a year: `1997`
- symbols: `!`
- a season: `spring`
- length greater than many normal weak passwords

To a strength meter, this can look strong because the password is longer and has different character types.

## 18. Why These Passwords Are Still Weak

The passwords are weak in a targeted attack because an attacker can guess the structure.

For example, an attacker could create rules like:

```text
symbol + year + season + common_word
common_word + year + symbol + season
role + year + symbol + season
season + year + symbol + name
```

Then the attacker could combine:

```text
seasons = summer, winter, spring, fall
roles = admin, user, test
years = 1990 through 2025
symbols = !, @, #, _
common_words = password leaks/common password lists
```

This would produce many passwords similar to the generated dataset.

So the password is not random. It is template-based.

That is the adversarial point:

> The password meter sees surface complexity, but the attacker sees a predictable generation process.

## 19. How to Run the Project

Open PowerShell and go to the project folder:

```powershell
cd C:\Users\husey\Desktop\InfoSecProject-FoolingPasswordTesters
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If that fails, use:

```powershell
python -m pip install -r requirements.txt
```

For the presentation demo, run:

```powershell
python combine.py
python summarize_results.py --examples 15
python analyze_patterns.py
```

To run the Flask frontend:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The dashboard includes:

- dataset summary metrics
- an instant demo generator
- generated password samples
- an interactive zxcvbn password checker
- rule-based attacker simulation results
- baseline comparison results
- a download link for the generated CSV

For the full pipeline, run:

```powershell
python clean_dataset.py
python modify_passwords.py
python score_password.py
python format_dataset.py
python train_model.py
python save_trained_model.py
python generate_passwords.py
python score_generated_passwords.py
python combine.py
python summarize_results.py
```

Important:

Training and generation can take a long time, especially on CPU. For a live presentation, use the demo commands instead of retraining the model.

If you are required to show training and generation live, use the shorter version:

```powershell
python train_model.py --max-records 200 --epochs 1 --save-steps 50 --logging-steps 10 --output-dir models/trained_model_demo
python save_trained_model.py --checkpoint models/trained_model_demo --output-dir models/final_model/demo_model
python generate_passwords.py --target 25 --batch-size 10 --model-dir models/final_model/demo_model --output data/generated_passwords/demo_generated_passwords.csv
python score_generated_passwords.py --input data/generated_passwords/demo_generated_passwords.csv --output data/generated_passwords/demo_verified_passwords.csv
python summarize_results.py --input data/generated_passwords/demo_verified_passwords.csv --examples 10
```

This does not recreate the full 19,574-password result, but it proves that the model training and generation path runs end to end.

## 20. What to Say During the Presentation

A strong explanation would be:

> We started with common weak passwords, then transformed them using predictable templates involving seasons, years, symbols, and common account-related words. We filtered those examples through `zxcvbn` and used the high-scoring examples to fine-tune Qwen2-0.5B with LoRA. The fine-tuned model then generated new passwords that also scored 4/4 on `zxcvbn`. Our merged dataset contains 19,574 unique generated passwords. The key finding is that these passwords look strong to the meter but remain vulnerable to targeted attacks because their structure is predictable.

If asked why the passwords are weak:

> They are weak because they are not truly random. Many are generated from small dictionaries of seasons, years, symbols, and common words. A targeted attacker could reproduce those templates with a rule-based cracking strategy.

If asked why `zxcvbn` gives them a high score:

> `zxcvbn` estimates guessing difficulty based on detected patterns and total guess count. These passwords often combine multiple components and have enough length that the estimated guess count becomes high, even though the components are semantically predictable.

If asked what the ML model contributes:

> The ML model learns the distribution of adversarial high-scoring passwords and generates new candidates that resemble that distribution, instead of manually hardcoding every output.

## 21. Limitations

The project has some limitations:

- It mainly evaluates `zxcvbn`, not every password meter.
- The generated passwords are visibly patterned, which is good for demonstrating weakness but may not cover all adversarial possibilities.
- The project does not run a full password-cracking benchmark with tools like Hashcat.
- Some claims about crackability are based on template predictability rather than measured cracking time.

These limitations are normal for a course project, but they should be mentioned honestly.

## 22. Future Work

Possible improvements:

- Test against more meters, such as Dropbox-style meters or web password forms.
- Run a real cracking experiment using Hashcat or John the Ripper.
- Generate a custom attack wordlist from the model templates.
- Compare model-generated adversarial passwords against random strong passwords.
- Train on a larger and more diverse dataset.
- Add metrics for template frequency and pattern distribution.

## 23. Final Conclusion

This project shows that password strength meters can be fooled by passwords with high surface complexity. The fine-tuned model generated more than 10,000 passwords that score highly on `zxcvbn`, but many still follow predictable patterns.

The main security lesson is:

> A high password-meter score does not always mean a password is safe from targeted guessing.
