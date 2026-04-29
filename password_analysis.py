import random
import re
import string

import pandas as pd
from zxcvbn import zxcvbn

from config import CLEANED_PASSWORDS_PATH, MERGED_GENERATED_PATH


SEASONS = ("spring", "summer", "fall", "winter")
ACCOUNT_WORDS = ("admin", "user", "test", "login", "pass", "password")
SYMBOLS = ("@", "!", "#", "_")
YEARS = tuple(str(year) for year in range(1990, 2026))

SYMBOL_PATTERN = re.compile(r"[^A-Za-z0-9]")
YEAR_PATTERN = re.compile(r"(19[9][0-9]|20[0-2][0-9])")


def load_passwords(path):
    df = pd.read_csv(path)
    if "password" not in df.columns:
        df = pd.read_csv(path, header=None, names=["password"])

    df = df.dropna(subset=["password"])
    df["password"] = df["password"].astype(str).str.strip()
    return df[df["password"].ne("")].drop_duplicates(subset=["password"]).reset_index(drop=True)


def load_generated_passwords():
    return load_passwords(MERGED_GENERATED_PATH)


def load_common_passwords():
    return load_passwords(CLEANED_PASSWORDS_PATH)


def has_any(text, words):
    lower = text.lower()
    return any(word in lower for word in words)


def classify(password):
    return {
        "contains_year": bool(YEAR_PATTERN.search(password)),
        "contains_season": has_any(password, SEASONS),
        "contains_account_word": has_any(password, ACCOUNT_WORDS),
        "contains_symbol": bool(SYMBOL_PATTERN.search(password)),
        "starts_with_symbol": bool(password and SYMBOL_PATTERN.match(password[0])),
        "contains_digit": any(ch.isdigit() for ch in password),
        "season_year_template": has_any(password, SEASONS) and bool(YEAR_PATTERN.search(password)),
        "account_year_template": has_any(password, ACCOUNT_WORDS) and bool(YEAR_PATTERN.search(password)),
    }


def pattern_summary(passwords):
    total = len(passwords)
    if total == 0:
        return {}

    features = pd.DataFrame([classify(password) for password in passwords])
    return {
        "contains_year": int(features["contains_year"].sum()),
        "contains_season": int(features["contains_season"].sum()),
        "contains_account_word": int(features["contains_account_word"].sum()),
        "contains_symbol": int(features["contains_symbol"].sum()),
        "starts_with_symbol": int(features["starts_with_symbol"].sum()),
        "contains_digit": int(features["contains_digit"].sum()),
        "season_year_template": int(features["season_year_template"].sum()),
        "account_year_template": int(features["account_year_template"].sum()),
    }


def percent(count, total):
    if total == 0:
        return "0.0%"
    return f"{count / total:.1%}"


def score_many(passwords):
    scores = [zxcvbn(password)["score"] for password in passwords]
    return {
        "avg_score": sum(scores) / len(scores) if scores else 0,
        "score_4_count": sum(1 for score in scores if score == 4),
        "scores": scores,
    }


def random_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#_"
    return "".join(random.choice(alphabet) for _ in range(length))


def make_random_passwords(count, length=16, seed=47205):
    random.seed(seed)
    return [random_password(length) for _ in range(count)]

