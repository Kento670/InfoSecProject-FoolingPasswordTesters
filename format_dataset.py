import argparse
import json

import pandas as pd


DEFAULT_INPUT = "data/training_dataset/training_dataset.csv"
DEFAULT_OUTPUT = "data/training_dataset/training_dataset.jsonl"
INSTRUCTION = "Generate a password that fools a strength meter:"


def main():
    parser = argparse.ArgumentParser(description="Format the password corpus as JSONL.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    with open(args.output, "w", encoding="utf-8") as f:
        for password in df["password"].dropna().astype(str):
            record = {"instruction": INSTRUCTION, "response": password}
            f.write(json.dumps(record) + "\n")

    print(f"Training JSONL file created and saved to {args.output}")


if __name__ == "__main__":
    main()
