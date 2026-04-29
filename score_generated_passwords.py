import argparse

import pandas as pd
from zxcvbn import zxcvbn

from config import DEFAULT_GENERATED_PATH, ZXCVBN_TARGET_SCORE


def read_passwords(path):
    df = pd.read_csv(path)
    if "password" not in df.columns:
        df = pd.read_csv(path, header=None, names=["password"])
    df = df[["password"]].dropna()
    df["password"] = df["password"].astype(str).str.strip()
    return df[df["password"].ne("")]


def score_passwords(df):
    rows = []
    for password in df["password"]:
        result = zxcvbn(password)
        rows.append(
            {
                "password": password,
                "zxcvbn_score": result["score"],
                "guesses": result["guesses"],
                "crack_time_offline_fast_hashing": result["crack_times_display"][
                    "offline_fast_hashing_1e10_per_second"
                ],
                "warning": result["feedback"].get("warning", ""),
            }
        )
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Score generated passwords with zxcvbn and keep the adversarial high-score subset."
    )
    parser.add_argument("--input", default=str(DEFAULT_GENERATED_PATH), help="CSV with a password column.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_GENERATED_PATH),
        help="Where to save scored passwords. Defaults to updating the input file.",
    )
    parser.add_argument("--min-score", type=int, default=ZXCVBN_TARGET_SCORE, help="Minimum zxcvbn score to keep.")
    args = parser.parse_args()

    df = read_passwords(args.input)
    scored = score_passwords(df).drop_duplicates(subset=["password"])
    verified = scored[scored["zxcvbn_score"] >= args.min_score].reset_index(drop=True)
    verified.to_csv(args.output, index=False)

    print(
        f"Done. Scored {len(scored)} generated passwords; "
        f"kept {len(verified)} scoring {args.min_score}+ in {args.output}"
    )


if __name__ == "__main__":
    main()
