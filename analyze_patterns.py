import argparse
import re

import pandas as pd

from config import MERGED_GENERATED_PATH


SEASONS = ("spring", "summer", "fall", "winter")
ACCOUNT_WORDS = ("admin", "user", "test", "login", "pass", "password")
SYMBOL_PATTERN = re.compile(r"[^A-Za-z0-9]")
YEAR_PATTERN = re.compile(r"(19[9][0-9]|20[0-2][0-9])")


def load_passwords(path):
    df = pd.read_csv(path)
    if "password" not in df.columns:
        df = pd.read_csv(path, header=None, names=["password"])
    df = df[["password"]].dropna()
    df["password"] = df["password"].astype(str).str.strip()
    return df[df["password"].ne("")].drop_duplicates()


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


def main():
    parser = argparse.ArgumentParser(
        description="Analyze predictable structures in generated adversarial passwords."
    )
    parser.add_argument("--input", default=str(MERGED_GENERATED_PATH), help="CSV with a password column.")
    parser.add_argument("--examples", type=int, default=8, help="Number of example passwords to print.")
    args = parser.parse_args()

    df = load_passwords(args.input)
    features = pd.DataFrame([classify(password) for password in df["password"]])
    analyzed = pd.concat([df.reset_index(drop=True), features], axis=1)

    print("Predictable pattern analysis")
    print("============================")
    print(f"File: {args.input}")
    print(f"Unique passwords analyzed: {len(analyzed):,}")
    print(f"Average length: {analyzed['password'].str.len().mean():.1f}")
    print()

    labels = {
        "contains_year": "Contains a year-like value",
        "contains_season": "Contains a season",
        "contains_account_word": "Contains account/common word",
        "contains_symbol": "Contains a symbol",
        "starts_with_symbol": "Starts with a symbol",
        "contains_digit": "Contains a digit",
        "season_year_template": "Contains both season and year",
        "account_year_template": "Contains both account word and year",
    }

    for column, label in labels.items():
        count = int(analyzed[column].sum())
        percent = count / len(analyzed)
        print(f"{label}: {count:,} ({percent:.1%})")

    print("\nExample predictable outputs:")
    example_rows = analyzed[
        analyzed["season_year_template"] | analyzed["account_year_template"] | analyzed["starts_with_symbol"]
    ]["password"].head(args.examples)
    for password in example_rows:
        print(f"  {password}")


if __name__ == "__main__":
    main()
