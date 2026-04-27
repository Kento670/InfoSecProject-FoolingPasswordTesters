import argparse

import pandas as pd
from zxcvbn import zxcvbn


DEFAULT_INPUT = "data/processed_dataset/modified_passwords.csv"
DEFAULT_OUTPUT = "data/training_dataset/training_dataset.csv"


def main():
    parser = argparse.ArgumentParser(
        description="Keep passwords that score high on zxcvbn for model training."
    )
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--min-score", type=int, default=3)
    parser.add_argument("--seed", type=int, default=47205)
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    scored_passwords = []
    for password in df["password"].dropna().astype(str):
        if zxcvbn(password)["score"] >= args.min_score:
            scored_passwords.append(password)

    df_scored = pd.DataFrame(scored_passwords, columns=["password"])
    df_scored = df_scored.sample(frac=1, random_state=args.seed).reset_index(drop=True)
    df_scored.to_csv(args.output, index=False)

    print(f"Training dataset saved to {args.output}")


if __name__ == "__main__":
    main()
