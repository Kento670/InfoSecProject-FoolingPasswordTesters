import argparse
from collections import Counter

import pandas as pd
from zxcvbn import zxcvbn


DEFAULT_INPUT = "data/new_dataset/common_passwords.csv"
DEFAULT_OUTPUT = "data/new_dataset/scored_common_passwords.csv"
DEFAULT_REPORT = "SOURCE_PASSWORD_REPORT.md"


def main():
    parser = argparse.ArgumentParser(
        description="Score the original online/common-password source dataset."
    )
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    rows = []

    for password in df["password"].dropna().astype(str):
        result = zxcvbn(password)
        rows.append(
            {
                "password": password,
                "zxcvbn_score": result["score"],
                "guesses": result["guesses"],
                "crack_time_offline_fast_hashing_1e10_per_second": result[
                    "crack_times_display"
                ]["offline_fast_hashing_1e10_per_second"],
            }
        )

    scored = pd.DataFrame(rows)
    scored.to_csv(args.output, index=False)

    counts = Counter(scored["zxcvbn_score"])
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("# Source Password Report\n\n")
        f.write(
            "This report scores the original online/common-password dataset used as the seed data.\n\n"
        )
        f.write(f"- Source file: `{args.input}`\n")
        f.write(f"- Passwords evaluated: {len(scored)}\n\n")
        f.write("## zxcvbn Score Distribution\n\n")
        for score in sorted(counts):
            f.write(f"- Score {score}: {counts[score]}\n")
        f.write("\n")
        f.write(
            "These source passwords are mostly weak by themselves. The project then modifies "
            "common-password material and fine-tunes a model to generate passwords that look "
            "stronger to zxcvbn while preserving predictable structure.\n"
        )

    print(f"Done. Source password scores saved to {args.output}")
    print(f"Done. Source password report saved to {args.report}")


if __name__ == "__main__":
    main()
