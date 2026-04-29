import argparse

from config import CLEANED_PASSWORDS_PATH, MERGED_GENERATED_PATH
from password_analysis import ACCOUNT_WORDS, SEASONS, SYMBOLS, YEARS, load_passwords


def generate_guesses(root_words):
    words = tuple(dict.fromkeys(tuple(root_words) + ACCOUNT_WORDS + SEASONS))
    for word in words:
        for season in SEASONS:
            for year in YEARS:
                for symbol in SYMBOLS:
                    yield f"{symbol}{year}{word}{season}"
                    yield f"{symbol}{year}{season}{word}"
                    yield f"{word}{year}{symbol}{season}"
                    yield f"{word}{year}{season}{symbol}"
                    yield f"{word}{symbol}{year}{season}"
                    yield f"{season}{year}{symbol}{word}"
                    yield f"{word}{season}{year}{symbol}"
                    yield f"{word}{year}{symbol}{season}{symbol}"


def simulate_attack(generated_path=MERGED_GENERATED_PATH, roots_path=CLEANED_PASSWORDS_PATH, max_roots=250):
    generated = load_passwords(generated_path)
    targets = set(generated["password"].astype(str))

    roots = load_passwords(roots_path)["password"].head(max_roots).astype(str).tolist()
    cracked = set()
    guesses = 0

    for guess in generate_guesses(roots):
        guesses += 1
        if guess in targets:
            cracked.add(guess)

    examples = sorted(cracked)[:10]
    return {
        "targets": len(targets),
        "guesses": guesses,
        "cracked": len(cracked),
        "cracked_percent": len(cracked) / len(targets) if targets else 0,
        "examples": examples,
        "max_roots": max_roots,
    }


def main():
    parser = argparse.ArgumentParser(description="Run a simple targeted rule-based attack simulation.")
    parser.add_argument("--input", default=str(MERGED_GENERATED_PATH), help="Generated password CSV.")
    parser.add_argument("--roots", default=str(CLEANED_PASSWORDS_PATH), help="Common password roots CSV.")
    parser.add_argument("--max-roots", type=int, default=250, help="Number of common roots to use.")
    args = parser.parse_args()

    result = simulate_attack(args.input, args.roots, args.max_roots)

    print("Rule-based attacker simulation")
    print("==============================")
    print(f"Targets: {result['targets']:,}")
    print(f"Rule guesses generated: {result['guesses']:,}")
    print(f"Recovered targets: {result['cracked']:,} ({result['cracked_percent']:.1%})")
    print(f"Common roots used: {result['max_roots']:,}")
    print("\nRecovered examples:")
    for password in result["examples"]:
        print(f"  {password}")


if __name__ == "__main__":
    main()

