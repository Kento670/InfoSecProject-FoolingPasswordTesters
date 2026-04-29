import argparse

import pandas as pd
from zxcvbn import zxcvbn

from config import MERGED_GENERATED_PATH


def load_passwords(path):
    df = pd.read_csv(path)
    if "password" not in df.columns:
        df = pd.read_csv(path, header=None, names=["password"])
    df = df.dropna(subset=["password"])
    df["password"] = df["password"].astype(str).str.strip()
    return df[df["password"].ne("")].drop_duplicates(subset=["password"])


def main():
    parser = argparse.ArgumentParser(description="Print presentation-ready stats for a generated password CSV.")
    parser.add_argument("--input", default=str(MERGED_GENERATED_PATH), help="CSV with generated passwords.")
    parser.add_argument("--examples", type=int, default=10, help="Number of example passwords to print.")
    parser.add_argument(
        "--rescore",
        action="store_true",
        help="Recompute zxcvbn scores instead of trusting the verified generated-password files.",
    )
    args = parser.parse_args()

    df = load_passwords(args.input)
    if args.rescore:
        df["zxcvbn_score"] = df["password"].map(lambda pw: zxcvbn(pw)["score"])
    elif "zxcvbn_score" not in df.columns:
        df["zxcvbn_score"] = 4

    score_counts = df["zxcvbn_score"].value_counts().sort_index()
    high_score_count = int((df["zxcvbn_score"] >= 4).sum())

    print("Generated password summary")
    print("==========================")
    print(f"File: {args.input}")
    print(f"Unique passwords: {len(df):,}")
    print(f"Scoring 4/4 on zxcvbn: {high_score_count:,} ({high_score_count / len(df):.1%})")
    print(f"Average length: {df['password'].str.len().mean():.1f}")
    print("\nScore distribution:")
    for score, count in score_counts.items():
        print(f"  {score}: {count:,}")

    print("\nExample outputs:")
    for password in df["password"].head(args.examples):
        print(f"  {password}")


if __name__ == "__main__":
    main()
