# 15-Minute Final Presentation Runbook

## Should This Be Enough For An A?

Yes, this is A-capable if presented carefully. The project has:

- a clear security research question
- a trained LoRA model artifact
- a working generator script
- a 10,000+ generated password dataset
- live reproducible scoring/evaluation scripts
- concrete results showing a mismatch between zxcvbn strength and targeted predictability

Do not claim that the project fully breaks every password meter. Claim that it demonstrates a measurable weakness in zxcvbn-style scoring under a targeted adversarial generation setup.

## Best One-Sentence Thesis

We fine-tuned a language model to generate passwords that look strong to zxcvbn, then showed that all 10,094 generated passwords scored 4 out of 4 while 90.17% still contained common-password material or predictable transformations.

## Timing Overview

| Time | Section | Goal |
| --- | --- | --- |
| 0:00-1:00 | Title and motivation | Explain the problem simply |
| 1:00-2:30 | Research question | Frame the security gap |
| 2:30-4:30 | Pipeline | Explain what you built |
| 4:30-6:00 | Model and data | Prove it is ML, not only rules |
| 6:00-8:30 | Live demo | Run evaluation and show output |
| 8:30-11:00 | Results and examples | Interpret the numbers |
| 11:00-12:30 | Why zxcvbn is fooled | Explain the mechanism |
| 12:30-14:00 | Limitations | Be honest and defensible |
| 14:00-15:00 | Conclusion | Land the research contribution |

## Before You Present

Open PowerShell before the presentation and run:

```powershell
cd "C:\Users\husey\Documents\New project\InfoSecProject-FoolingPasswordTesters"
```

Have these ready:

```powershell
Get-Content ATTACKABILITY_REPORT.md
Get-Content data/generated_passwords/scored_generated_passwords.csv -TotalCount 8
Get-Content data/generated_passwords/attackability_results.csv -TotalCount 8
dir models\final_model\final_model_v4
```

If you want to rerun live:

```powershell
python score_generated_passwords.py `
  --input data/generated_passwords/verified_passwords_v1.csv `
  --output data/generated_passwords/scored_generated_passwords.csv

python evaluate_attackability.py `
  --generated data/generated_passwords/verified_passwords_v1.csv `
  --output data/generated_passwords/attackability_results.csv `
  --report ATTACKABILITY_REPORT.md
```

## Slide-by-Slide Talk Track

### Slide 1: Title

Say:

"Our project is about adversarial machine learning against password strength meters. The main question is whether a model can generate passwords that look strong to a meter, but are still predictable to an attacker."

"Our final result is: 10,094 generated passwords, all scoring 4 out of 4 on zxcvbn, with 90.17% still matching our targeted attackability check."

Do not spend too long here. This slide is just the hook.

### Slide 2: Research Question

Say:

"Password meters are useful, but they are still scoring algorithms. zxcvbn estimates how guessable a password is by looking for known patterns, dictionaries, dates, repeated strings, and other features."

"The problem is that attackers do not guess uniformly at random. They use dictionaries, leaked passwords, years, names, and transformation rules. So our research question became: can we train or guide a model to generate passwords that satisfy the meter while preserving predictable structure?"

Key phrase:

"The gap is between perceived strength and targeted attack resistance."

### Slide 3: System Pipeline

Say:

"The pipeline starts with common passwords. We clean them, create adversarial variants by appending or prepending patterns, score those variants with zxcvbn, and use the high-scoring examples as training data."

"Then we fine-tune Qwen2-0.5B using LoRA. The generator samples candidate passwords from the fine-tuned adapter. Finally, we filter the outputs through zxcvbn and keep passwords that score 4."

"The final step is important: we do not stop at 'the meter says strong.' We run a targeted evaluation to ask whether the generated password still contains common-password material."

### Slide 4: Model and Implementation

Say:

"The model is Qwen2-0.5B with a LoRA adapter. LoRA lets us fine-tune a smaller number of adapter weights rather than retraining the entire base model."

"The repo contains the final adapter model files and checkpoint files. This matters because it shows this is not just a prompt or a hand-written list; there is a trained model artifact."

Optional live proof:

```powershell
dir models\final_model\final_model_v4
```

Point out:

- `adapter_model.safetensors`
- `adapter_config.json`

### Slide 5: Live Demo Commands

Say:

"For the live demo, I am not going to retrain the model because that takes too long. Instead, I will rerun the fast evaluation scripts on the generated dataset."

Run:

```powershell
python score_generated_passwords.py `
  --input data/generated_passwords/verified_passwords_v1.csv `
  --output data/generated_passwords/scored_generated_passwords.csv
```

Say:

"This script scores the generated passwords using zxcvbn and writes the score, estimated guesses, crack-time display, and match sequence count."

Then run:

```powershell
python evaluate_attackability.py `
  --generated data/generated_passwords/verified_passwords_v1.csv `
  --output data/generated_passwords/attackability_results.csv `
  --report ATTACKABILITY_REPORT.md
```

Say:

"This checks whether high-scoring generated passwords still contain common-password material or predictable transformations."

Then run:

```powershell
Get-Content ATTACKABILITY_REPORT.md
```

Pause and point to:

- Generated passwords evaluated: 10094
- Score 4: 10094
- Overall targeted-match rate: 90.17%

### Slide 6: Main Result

Say:

"This is the central result. We evaluated 10,094 generated passwords. Every one of them scored 4 on zxcvbn."

"But 9,102 of them were still matched by the targeted attackability analysis. That means they contain common-password material or predictable structure that an attacker could prioritize."

"So the project shows that a high zxcvbn score is not always the same as resistance to targeted guessing."

If you need one strong sentence:

"The meter is measuring one model of guessability; our attacker uses a different, project-specific model."

### Slide 7: Real Examples

Say:

"Here are actual examples from the generated dataset, not made-up examples."

Use examples:

- `!1990summersage`
- `!1993#testuser`
- `!1996_aleksandar`
- `!1999falldavid`
- `!1995spring2010jane`

Say:

"These all score 4 on zxcvbn. But to a human attacker, the structure is visible: years, seasons, names, common words, and symbols. That is exactly the adversarial gap."

Optional command:

```powershell
Get-Content data/generated_passwords/scored_generated_passwords.csv -TotalCount 8
```

### Slide 8: Why zxcvbn Is Fooled

Say:

"zxcvbn is not a bad tool. It is actually much better than simple composition rules. But no meter can perfectly know the attacker's custom generation process."

"These passwords get credit for being longer and combining symbols, years, and words. But if the attacker knows the construction pattern, the search space becomes much smaller than true randomness."

Say this carefully:

"The attack does not need to search every possible 14-character password. It searches common passwords combined with a small set of phrases, years, and symbols."

### Slide 9: Limitations

Say:

"There are three main limitations. First, we directly evaluated zxcvbn, not the Dropbox meter. Second, our attackability check is a targeted rule-set analysis, not a full hashcat benchmark. Third, about 9.83% of outputs were not matched by this specific targeted check."

"But these limitations do not invalidate the result. The project demonstrates feasibility: generated passwords can get maximum meter scores while preserving predictable structure."

This is where you sound mature and research-oriented.

### Slide 10: Conclusion

Say:

"The takeaway is not that password meters are useless. The takeaway is that strength meters are approximations, and adversarial generation can exploit the assumptions behind those approximations."

"Our contribution is a working pipeline and dataset showing that a fine-tuned language model can generate zxcvbn-high passwords that are still predictable under targeted analysis."

End with:

"A high password meter score should not be treated as proof of resistance against targeted guessing."

## Likely Professor Questions and Answers

### Q: Is this really machine learning, or just rule-based generation?

Answer:

"Both are involved, but in different stages. The rule-based part creates adversarial training examples from common passwords. Then Qwen2-0.5B is fine-tuned with LoRA on those examples, and the generator samples from the trained adapter. The repo includes the adapter model files and checkpoint."

### Q: Why did you use zxcvbn?

Answer:

"zxcvbn is open-source, widely used, and exposes a 0-4 score plus useful guessability metadata. That made it practical to evaluate reproducibly. We frame the result as zxcvbn-specific rather than claiming all meters are broken."

### Q: Did you actually crack the passwords?

Answer:

"We did not run a full hashcat or John the Ripper benchmark. Instead, we measured targeted attackability by checking whether outputs match common-password material and predictable transformations. A full cracking benchmark would be the strongest next step."

### Q: If the targeted search space is 80.6 million, is that really small?

Answer:

"Yes, relative to random password search. A true random password of similar length over letters, digits, and symbols has an enormous search space. 80.6 million candidates is small enough to prioritize in an offline attack, especially compared with exhaustive search."

### Q: Why do all passwords scoring 4 matter?

Answer:

"Because score 4 is zxcvbn's strongest category. If every generated password reaches that category, but most still preserve targeted patterns, then the meter's top score is not sufficient evidence of actual attack resistance."

### Q: What does 'contains_common_password' mean?

Answer:

"It means the generated password contains material from the common-password dataset after normalization. For example, symbols and leetspeak are normalized, then the script checks for common-password components and known transformation patterns."

### Q: What would improve this project?

Answer:

"Three things: evaluate more meters, especially Dropbox-style scoring; run a real cracking benchmark using hashcat or John; and train on more diverse adversarial examples to compare how pattern complexity affects meter scores."

### Q: Could zxcvbn be updated to catch this?

Answer:

"Partly. Meters could add better detection for generated or concatenated dictionary patterns, but there is always a cat-and-mouse problem. If attackers know the features, they can search for inputs just outside those features."

### Q: Is this ethical?

Answer:

"Yes, because the project uses synthetic/generated passwords and common public datasets to evaluate defensive tools. The goal is to understand weaknesses in strength meters so they can be improved."

## If Something Breaks During Demo

If a script takes too long or errors, do not panic. Run:

```powershell
Get-Content ATTACKABILITY_REPORT.md
```

Then say:

"The evaluation has already been run and the report is committed locally. The live script regenerates this report, but the key result is here."

If asked to show the dataset:

```powershell
Get-Content data/generated_passwords/verified_passwords_v1.csv -TotalCount 10
```

If asked to show scores:

```powershell
Get-Content data/generated_passwords/scored_generated_passwords.csv -TotalCount 10
```

If asked to show model files:

```powershell
dir models\final_model\final_model_v4
```

## How To Use Your Friend's Slides

Your friend's deck is useful for process history, especially the slides about the four training attempts. But for the final presentation, do not spend too much time on every version.

Use that material as:

- one quick "experimentation history" section
- evidence that you iterated on pattern complexity
- backup if someone asks how the dataset evolved

For the final grade, prioritize:

- research question
- working pipeline
- live demo
- final metrics
- honest limitations

