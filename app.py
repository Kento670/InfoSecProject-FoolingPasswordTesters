import random
from functools import lru_cache

from flask import Flask, render_template, request, send_file
from zxcvbn import zxcvbn

from baseline_comparison import compare_baselines
from config import MERGED_GENERATED_PATH
from password_analysis import (
    ACCOUNT_WORDS,
    SEASONS,
    SYMBOLS,
    YEARS,
    classify,
    load_generated_passwords,
    pattern_summary,
    percent,
)
from rule_attack_simulation import simulate_attack


app = Flask(__name__)


@lru_cache(maxsize=1)
def cached_generated_passwords():
    return load_generated_passwords()


@lru_cache(maxsize=1)
def cached_attack_result():
    return simulate_attack(max_roots=100)


@lru_cache(maxsize=1)
def cached_baselines():
    return compare_baselines(sample_size=150)


def score_password(password):
    result = zxcvbn(password)
    crack_times = result["crack_times_display"]
    flags = classify(password)
    return {
        "password": password,
        "score": result["score"],
        "guesses": f"{int(result['guesses']):,}",
        "offline_fast_hashing": crack_times["offline_fast_hashing_1e10_per_second"],
        "online_no_throttling": crack_times["online_no_throttling_10_per_second"],
        "warning": result.get("feedback", {}).get("warning", ""),
        "features": [
            {"label": "year", "active": flags["contains_year"]},
            {"label": "season", "active": flags["contains_season"]},
            {"label": "account word", "active": flags["contains_account_word"]},
            {"label": "symbol", "active": flags["contains_symbol"]},
            {"label": "digit", "active": flags["contains_digit"]},
        ],
    }


def make_manual_adversarial_passwords(count=5):
    random.seed()
    words = tuple(dict.fromkeys(ACCOUNT_WORDS + SEASONS))
    passwords = []
    while len(passwords) < count:
        word = random.choice(words)
        season = random.choice(SEASONS)
        year = random.choice(YEARS)
        symbol = random.choice(SYMBOLS)
        templates = (
            f"{symbol}{year}{word}{season}",
            f"{word}{year}{symbol}{season}",
            f"{season}{year}{symbol}{word}",
            f"{word}{symbol}{year}{season}",
        )
        candidate = random.choice(templates)
        if zxcvbn(candidate)["score"] >= 4:
            passwords.append(candidate)
    return passwords


def dataset_cards(df):
    total = len(df)
    patterns = pattern_summary(df["password"].tolist())
    return [
        {"label": "Generated passwords", "value": f"{total:,}"},
        {"label": "Score 4/4 on zxcvbn", "value": f"{total:,}"},
        {"label": "Contain years", "value": percent(patterns["contains_year"], total)},
        {"label": "Contain season + year", "value": percent(patterns["season_year_template"], total)},
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    df = cached_generated_passwords()
    entered_password = ""
    score_result = None
    generated_now = []

    if request.method == "POST":
        action = request.form.get("action")
        if action == "score":
            entered_password = request.form.get("password", "").strip()
            score_result = score_password(entered_password) if entered_password else None
        elif action == "generate":
            generated_now = make_manual_adversarial_passwords(count=5)

    sample_passwords = df["password"].sample(n=min(8, len(df)), random_state=47205).tolist()
    attack_result = cached_attack_result()
    baselines = cached_baselines()

    return render_template(
        "index.html",
        cards=dataset_cards(df),
        entered_password=entered_password,
        score_result=score_result,
        generated_now=generated_now,
        sample_passwords=sample_passwords,
        attack_result=attack_result,
        baselines=baselines,
    )


@app.route("/download/generated")
def download_generated():
    return send_file(MERGED_GENERATED_PATH, as_attachment=True, download_name="verified_passwords_1+5.csv")


if __name__ == "__main__":
    app.run(debug=False)
