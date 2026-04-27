import argparse
import random

import pandas as pd


DEFAULT_INPUT = "data/processed_dataset/cleaned_dataset.csv"
DEFAULT_OUTPUT = "data/processed_dataset/modified_passwords.csv"

PHRASES = ["summer", "winter", "fall", "spring", "test", "admin", "user"]
SYMBOLS = ["@", "!", "#", "_"]
YEARS = list(range(1990, 2026))


def generate_pattern():
    phrase = random.choice(PHRASES)
    symbol = random.choice(SYMBOLS)
    year = str(random.choice(YEARS))

    return random.choice(
        [
            f"{phrase}{symbol}{year}",
            f"{year}{symbol}{phrase}",
            f"{phrase}{year}{symbol}",
            f"{symbol}{year}{phrase}",
        ]
    )


def build_modified_passwords(passwords, variants_per_password):
    modified_passwords = []

    for password in passwords:
        modified_passwords.append(password)

        for _ in range(variants_per_password):
            pattern = generate_pattern()
            modified_passwords.append(password + pattern)
            modified_passwords.append(pattern + password)

    return modified_passwords


def main():
    parser = argparse.ArgumentParser(
        description="Create weak-looking-but-meter-friendly password variants."
    )
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--variants-per-password", type=int, default=3)
    parser.add_argument("--seed", type=int, default=47205)
    args = parser.parse_args()

    random.seed(args.seed)

    df = pd.read_csv(args.input)
    passwords = df["password"].dropna().astype(str).tolist()
    modified_passwords = build_modified_passwords(passwords, args.variants_per_password)

    output_df = pd.DataFrame(modified_passwords, columns=["password"])
    output_df = output_df.drop_duplicates()
    output_df.to_csv(args.output, index=False)

    print(f"Done. Modified password dataset saved to {args.output}")


if __name__ == "__main__":
    main()
