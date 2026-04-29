import argparse

from config import CLEANED_PASSWORDS_PATH, MERGED_GENERATED_PATH
from password_analysis import (
    load_passwords,
    make_random_passwords,
    pattern_summary,
    percent,
    score_many,
)


def summarize_dataset(name, passwords):
    scores = score_many(passwords)
    patterns = pattern_summary(passwords)
    total = len(passwords)
    return {
        "name": name,
        "count": total,
        "avg_length": sum(len(password) for password in passwords) / total if total else 0,
        "avg_score": scores["avg_score"],
        "score_4": scores["score_4_count"],
        "score_4_percent": percent(scores["score_4_count"], total),
        "season_year": patterns.get("season_year_template", 0),
        "season_year_percent": percent(patterns.get("season_year_template", 0), total),
        "year": patterns.get("contains_year", 0),
        "year_percent": percent(patterns.get("contains_year", 0), total),
    }


def compare_baselines(sample_size=500):
    common = load_passwords(CLEANED_PASSWORDS_PATH)["password"].head(sample_size).astype(str).tolist()
    generated = load_passwords(MERGED_GENERATED_PATH)["password"].head(sample_size).astype(str).tolist()

    avg_generated_length = round(sum(len(password) for password in generated) / len(generated))
    random_passwords = make_random_passwords(sample_size, length=avg_generated_length)

    return [
        summarize_dataset("Common weak passwords", common),
        summarize_dataset("Generated adversarial", generated),
        summarize_dataset("Random baseline", random_passwords),
    ]


def main():
    parser = argparse.ArgumentParser(description="Compare generated adversarial passwords to baseline datasets.")
    parser.add_argument("--sample-size", type=int, default=500, help="Rows to score from each dataset.")
    args = parser.parse_args()

    rows = compare_baselines(args.sample_size)

    print("Baseline comparison")
    print("===================")
    for row in rows:
        print(f"\n{row['name']}")
        print(f"  Count scored: {row['count']:,}")
        print(f"  Average length: {row['avg_length']:.1f}")
        print(f"  Average zxcvbn score: {row['avg_score']:.2f}/4")
        print(f"  Score 4/4: {row['score_4']:,} ({row['score_4_percent']})")
        print(f"  Contains year: {row['year']:,} ({row['year_percent']})")
        print(f"  Contains season+year: {row['season_year']:,} ({row['season_year_percent']})")


if __name__ == "__main__":
    main()

