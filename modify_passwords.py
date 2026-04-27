import pandas as pd
import random
import string

processed_dataset_path = "data/processed_dataset/cleaned_dataset.csv"
training_dataset_path = "data/processed_dataset/modified_passwords.csv"


phrases = ["summer", "winter", "fall", "spring", "test", "admin", "user"]
symbols = ["@", "!", "#", "_",]
years = list(range(1990, 2025))

def generate_pattern():
    phrase = random.choice(phrases)
    symbol = random.choice(symbols)
    year = str(random.choice(years))

    formats = [
        f"{phrase}{symbol}{year}",
        f"{year}{symbol}{phrase}",
        f"{phrase}{year}{symbol}",
        f"{symbol}{year}{phrase}",
    ]

    return random.choice(formats)

"""
for v2
symbols = [
    "!", "#", "$", "%", "&", 
    "'", "(", ")", "*", "+", ",",
    "-", ".", ":", ";", "<", 
    "=", ">", "?", "@", "[",  
    "]", "^", "_", "`", "{", "|", 
    "}", "~"
]
years = list(range(1990, 2025))

substitutions = {
    "a": "@", "A": "@",
    "e": "3", "E": "3",
    "i": "1", "I": "1",
    "l": "1", "L": "1",
    "o": "0", "O": "0",
    "s": "$", "S": "$",
}
"""

"""
for v3

symbols = [
    "!", "#", "$", "%", "&", 
    "'", "*", "+", ",",
    "-", ".", ":", ";", 
    "?", "_",
]

#years = list(range(1999, 2026))

substitutions = {
    "a": "@", "A": "@",
    "e": "3", "E": "3",
    "o": "0", "O": "0",
    "s": "$", "S": "$",
}

def generate_pattern():
    symbol = random.choice(symbols)
    #year = str(random.choice(years))

    formats = [
        #f"{symbol}{year}",
        #f"{year}{symbol}",
        f"{symbol}",
    ]

    return random.choice(formats)
"""


def substitute(pw, subs):
    possible = [ch for ch in pw if ch in subs]
    if not possible:
        return pw
    
    target = random.choice(possible)
    return pw.replace(target, subs[target], 1)

def capitalize(pw):
    letters = [i for i, ch in enumerate(pw) if ch.isalpha()]
    if not letters:
        return pw
    
    random_letter = random.choice(letters)
    return pw[:random_letter] + pw[random_letter].upper() + pw[random_letter+1:]

def random_symbol(pw, symbols):
    if not pw:
        return pw
    
    symbol = random.choice(symbols)
    idx = random.randint(0, len(pw))  # inclusive of end position
    return pw[:idx] + symbol + pw[idx:]


df = pd.read_csv(processed_dataset_path)
passwords = df['password'].tolist()

modified_passwords = []

for pw in passwords:
    modified_passwords.append(pw)

    for _ in range(1):
        pattern = generate_pattern()
        modified_passwords.append(pw + pattern)
        modified_passwords.append(pattern + pw)

    """
        for v1
    
        for _ in range(3):
        pattern = generate_pattern()

        modified_passwords.append(pw + pattern)
        modified_passwords.append(pattern + pw)
    """

    """
        for v2

        substituted_password = substitute(pw, substitutions)
        modified_passwords.append(substituted_password)

        for _ in range(6):
            pattern1 = generate_pattern()
            pattern2 = generate_pattern()

            modified_passwords.append(pw + pattern1)
            modified_passwords.append(pattern2 + pw)

            modified_passwords.append(substituted_password + pattern1)
            modified_passwords.append(pattern2 + substituted_password)
    """


    """
    substituted_password = substitute(pw, substitutions)
    capitalized_password = capitalize(pw)
    capitalized_sub_password = capitalize(substituted_password)
    symbol_password = random_symbol(pw, symbols)


    #modified_passwords.append(symbol_password)
    modified_passwords.append(substituted_password)
    modified_passwords.append(capitalized_password)
    modified_passwords.append(capitalized_sub_password)

    for _ in range(1):

        modified_passwords.append(random_symbol(pw, symbols))
        modified_passwords.append(random_symbol(substituted_password, symbols))
        modified_passwords.append(random_symbol(capitalized_password, symbols))
        modified_passwords.append(random_symbol(capitalized_sub_password, symbols))

        "
        for v3

        pattern1 = generate_pattern()
        pattern2 = generate_pattern()
        

        if random.random() < 0.5:
            modified_passwords.append(pw + pattern1)
        else:
            modified_passwords.append(pattern1 + pw)

        if random.random() < 0.5:
            modified_passwords.append(substituted_password + pattern2)
        else:
            modified_passwords.append(pattern2 + substituted_password)

        if random.random() < 0.5:
            modified_passwords.append(capitalized_password + pattern1)
        else:
            modified_passwords.append(pattern1 + capitalized_password)

        if random.random() < 0.5:
            modified_passwords.append(capitalized_sub_password + pattern2)
        else:
            modified_passwords.append(pattern2 + capitalized_sub_password)
        "
    """
    


df = pd.DataFrame(modified_passwords, columns=['password'])
df = df.drop_duplicates()

df.to_csv(training_dataset_path, index=False)

print(f"Done. Combined Passwords dataset saved to {training_dataset_path}")
