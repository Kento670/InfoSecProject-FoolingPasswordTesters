# Source Password Report

This report scores the original online/common-password dataset used as the seed data.

- Source file: `data/new_dataset/common_passwords.csv`
- Passwords evaluated: 10000

## zxcvbn Score Distribution

- Score 0: 3463
- Score 1: 6536
- Score 2: 1

These source passwords are mostly weak by themselves. The project then modifies common-password material and fine-tunes a model to generate passwords that look stronger to zxcvbn while preserving predictable structure.
