import argparse

import pandas as pd
from zxcvbn import zxcvbn


DEFAULT_INPUT = "data/generated_passwords/verified_passwords_v1.csv"
DEFAULT_OUTPUT = "data/generated_passwords/scored_generated_passwords.csv"


def score_password(password):
    result = zxcvbn(password)
    return {
        "password": password,
        "zxcvbn_score": result["score"],
        "guesses": result["guesses"],
        "crack_time_offline_fast_hashing_1e10_per_second": result["crack_times_display"][
            "offline_fast_hashing_1e10_per_second"
        ],
        "matched_sequence_count": len(result["sequence"]),
    }


def main():
    parser = argparse.ArgumentParser(description="Score generated passwords with zxcvbn.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    rows = [score_password(password) for password in df["password"].dropna().astype(str)]
    scored_df = pd.DataFrame(rows)
    scored_df.to_csv(args.output, index=False)

    print(f"Done. Scored generated passwords saved to {args.output}")


if __name__ == "__main__":
    main()
