from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"
NEW_DATASET_DIR = DATA_DIR / "new_dataset"
PROCESSED_DATASET_DIR = DATA_DIR / "processed_dataset"
TRAINING_DATASET_DIR = DATA_DIR / "training_dataset"
GENERATED_PASSWORDS_DIR = DATA_DIR / "generated_passwords"
MODEL_DIR = ROOT_DIR / "models"

RAW_PASSWORDS_PATH = NEW_DATASET_DIR / "common_passwords.csv"
CLEANED_PASSWORDS_PATH = PROCESSED_DATASET_DIR / "cleaned_dataset.csv"
MODIFIED_PASSWORDS_PATH = PROCESSED_DATASET_DIR / "modified_passwords.csv"
TRAINING_DATASET_PATH = TRAINING_DATASET_DIR / "training_dataset.csv"
TRAINING_JSONL_PATH = TRAINING_DATASET_DIR / "training_dataset.jsonl"

BASE_MODEL_NAME = "Qwen/Qwen2-0.5B"
TRAINED_MODEL_DIR = MODEL_DIR / "trained_model"
FINAL_MODEL_DIR = MODEL_DIR / "final_model" / "final_model_v5"

DEFAULT_GENERATED_PATH = GENERATED_PASSWORDS_DIR / "verified_passwords_v5.csv"
MERGED_GENERATED_PATH = GENERATED_PASSWORDS_DIR / "verified_passwords_1+5.csv"

ZXCVBN_TARGET_SCORE = 4
