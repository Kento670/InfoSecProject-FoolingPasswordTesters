import path from "node:path";
import fs from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";

const runtimeRoot = "C:/Users/husey/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool";
const artifact = await import(pathToFileURL(`${runtimeRoot}/dist/artifact_tool.mjs`).href);

const {
  Presentation,
  PresentationFile,
  row,
  column,
  grid,
  panel,
  text,
  rule,
  fill,
  hug,
  fixed,
  wrap,
  fr,
} = artifact;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const outDir = path.resolve(__dirname, "../slides/output");

const W = 1920;
const H = 1080;
const C = {
  bg: "#F6F8FB",
  ink: "#152033",
  muted: "#627083",
  line: "#DCE3EC",
  blue: "#185ABC",
  teal: "#00796B",
  red: "#B13B3B",
  orange: "#A45B00",
  dark: "#111827",
  white: "#FFFFFF",
  softBlue: "#EAF1FF",
  softTeal: "#EAF7F5",
  softOrange: "#FFF4E5",
};

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

function addSlide(body, notes, opts = {}) {
  const slide = presentation.slides.add();
  slide.compose(
    panel(
      {
        name: "slide-root",
        width: fill,
        height: fill,
        fill: opts.fill ?? C.bg,
        padding: { x: 92, y: 64 },
      },
      body,
    ),
    { frame: { left: 0, top: 0, width: W, height: H }, baseUnit: 8 },
  );
  slide.speakerNotes.setText(notes);
  return slide;
}

function title(value, size = 54, color = C.ink) {
  return text(value, {
    name: "slide-title",
    width: fill,
    height: hug,
    style: { fontSize: size, bold: true, color },
  });
}

function subtitle(value, size = 26, color = C.muted) {
  return text(value, {
    name: "slide-subtitle",
    width: fill,
    height: hug,
    style: { fontSize: size, color },
  });
}

function label(value, color = C.teal) {
  return text(value, {
    width: fill,
    height: hug,
    style: { fontSize: 17, bold: true, color },
  });
}

function metric(value, description, color = C.blue, valueSize = 50) {
  return column({ width: fill, height: hug, gap: 6 }, [
    text(value, { width: fill, height: hug, style: { fontSize: valueSize, bold: true, color } }),
    text(description, { width: fill, height: hug, style: { fontSize: 19, color: C.muted } }),
  ]);
}

function bullet(head, body) {
  return row({ width: fill, height: hug, gap: 18, align: "start" }, [
    panel({ width: fixed(14), height: fixed(14), fill: C.blue, borderRadius: "rounded-full" }),
    column({ width: fill, height: hug, gap: 4 }, [
      text(head, { width: fill, height: hug, style: { fontSize: 27, bold: true, color: C.ink } }),
      text(body, { width: fill, height: hug, style: { fontSize: 21, color: C.muted } }),
    ]),
  ]);
}

function chip(value, fillColor = C.softBlue, color = C.blue) {
  return panel({ width: hug, height: hug, fill: fillColor, borderRadius: "rounded-full", padding: { x: 18, y: 10 } },
    text(value, { width: hug, height: hug, style: { fontSize: 19, bold: true, color } }));
}

function step(num, head, body) {
  return panel({ fill: C.white, line: { color: C.line, width: 1 }, borderRadius: 12, padding: 18 },
    column({ width: fill, height: hug, gap: 8 }, [
      text(num, { width: fill, height: hug, style: { fontSize: 26, bold: true, color: C.blue } }),
      text(head, { width: fill, height: hug, style: { fontSize: 21, bold: true, color: C.ink } }),
      text(body, { width: fill, height: hug, style: { fontSize: 15, color: C.muted } }),
    ]));
}

function bar(name, pct, count, color) {
  return grid({ width: fill, height: fixed(72), columns: [fr(1.05), fr(1.5), fixed(140)], columnGap: 18, alignItems: "center" }, [
    column({ width: fill, height: hug, gap: 3 }, [
      text(name, { width: fill, height: hug, style: { fontSize: 21, bold: true, color: C.ink } }),
      text(count, { width: fill, height: hug, style: { fontSize: 15, color: C.muted } }),
    ]),
    panel({ width: fill, height: fixed(18), fill: "#E5EAF1", borderRadius: "rounded-full" },
      panel({ width: fixed(Math.round(690 * pct)), height: fixed(18), fill: color, borderRadius: "rounded-full" })),
    text(`${Math.round(pct * 1000) / 10}%`, { width: fill, height: hug, style: { fontSize: 25, bold: true, color: C.ink } }),
  ]);
}

function table(headers, rows) {
  return column({ width: fill, height: hug, gap: 0 }, [
    row({ width: fill, height: fixed(52), gap: 0 }, headers.map((h) =>
      panel({ width: fill, height: fill, fill: "#EEF3F8", padding: { x: 12, y: 12 } },
        text(h, { width: fill, height: hug, style: { fontSize: 18, bold: true, color: C.ink } })))),
    ...rows.map((r) => row({ width: fill, height: fixed(62), gap: 0 }, r.map((cell, i) =>
      panel({ width: fill, height: fill, fill: i === 0 ? "#FAFBFD" : C.white, line: { color: C.line, width: 1 }, padding: { x: 12, y: 14 } },
        text(cell, { width: fill, height: hug, style: { fontSize: 18, bold: i === 0, color: i === 0 ? C.ink : C.muted } }))))),
  ]);
}

const notes = [
  `Open by saying: Our project is about whether a password strength meter can be fooled. We trained and tested a pipeline that creates passwords that look strong to zxcvbn, but still follow predictable patterns. The key framing is not "we made secure passwords." It is "we made passwords that the meter thinks are secure."`,
  `Say: Password meters are useful, but they are still algorithms. They reward features like length, symbols, numbers, and estimated guessing cost. Attackers can look for the gap between what the meter rewards and what targeted guessing can exploit.`,
  `Say: zxcvbn is smarter than a basic checklist. It looks for dictionary words, dates, repeats, sequences, and patterns, then estimates guesses. Our attack takes advantage of passwords that combine enough pieces to score high, even when those pieces are semantically predictable.`,
  `Say: Our research question is whether ML can generate high-scoring passwords that are not truly random. The deliverables are a generation script, a fine-tuned LLM, and more than 10,000 adversarial passwords. We satisfy all three.`,
  `Say: We started from common weak passwords, then added predictable complexity: seasons, years, symbols, and account words. This matters because the weak root is still there. We are not creating random secrets; we are creating structured passwords that look complex.`,
  `Say: This is the full pipeline. Clean the data, transform weak passwords, keep high zxcvbn examples, format as JSONL, fine-tune Qwen2-0.5B with LoRA, generate new candidates, then analyze the results. For the demo, the expensive model work is precomputed.`,
  `Say: The model is Qwen2-0.5B with LoRA. LoRA trains a small adapter instead of the whole model, which makes it feasible for a course project. The prompt is simple: generate a password that fools a strength meter. We filter model outputs with zxcvbn.`,
  `Say: The merged dataset has 19,574 unique generated passwords. All score 4 out of 4 on zxcvbn. The average length is 16.5 characters. These numbers directly satisfy the dataset and high-score generation requirements.`,
  `Say: This is the important weakness evidence. 99.2 percent contain a year-like value, 84.5 percent contain a season, 96.7 percent contain a symbol, and 83.8 percent contain both season and year. That means the outputs are high-scoring but heavily patterned.`,
  `Say: To make the weakness argument stronger, we added a rule-based attacker simulation. Using only 100 common roots plus years, seasons, and symbols, it generated about 488,000 guesses and recovered 2,808 passwords, or 14.3 percent of the dataset.`,
  `Say: The baseline comparison shows why this is adversarial. Random passwords also score 4 out of 4, but they do not contain season-year templates. Generated adversarial passwords score like random passwords, but pattern like weak passwords.`,
  `Say: The Flask app is the live demo. It is intentionally simple: check a password, generate a few examples, see attack results, compare baselines, and download the CSV. Do not spend too long here. Show the app, score one example, click Generate 5, and point to the attacker result.`,
  `Say: Limitations: we focused mainly on zxcvbn and did not run a full Hashcat benchmark. Future work would test more meters and do real cracking experiments. Conclusion: a high password meter score does not always mean resistance to targeted guessing.`,
];

// 1
addSlide(grid({ width: fill, height: fill, columns: [fr(1.05), fr(0.95)], columnGap: 60, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 24 }, [
    label("Project 4 | Information Security"),
    text("Adversarial ML Against Password Strength Meters", { width: fill, height: hug, style: { fontSize: 72, bold: true, color: C.ink } }),
    subtitle("Generating passwords that score strong while staying predictable enough for targeted attacks."),
    row({ width: fill, height: hug, gap: 12 }, [chip("zxcvbn 4/4"), chip("LoRA fine-tuned LLM", C.softTeal, C.teal), chip("19,574 generated passwords", C.softOrange, C.orange)]),
  ]),
  panel({ width: fill, height: fixed(650), fill: C.dark, borderRadius: 18, padding: { x: 36, y: 38 } },
    column({ width: fill, height: fill, gap: 18 }, [
      text("> Generate a password that fools a strength meter", { width: fill, height: hug, style: { fontSize: 25, color: "#A7F3D0" } }),
      rule({ width: fill, stroke: "#334155", weight: 2 }),
      text("@2021userfall", { width: fill, height: hug, style: { fontSize: 40, bold: true, color: C.white } }),
      text("admin1997!spring!", { width: fill, height: hug, style: { fontSize: 40, bold: true, color: C.white } }),
      text("#2015springfalluser", { width: fill, height: hug, style: { fontSize: 40, bold: true, color: C.white } }),
      text("_1995winterfall", { width: fill, height: hug, style: { fontSize: 40, bold: true, color: C.white } }),
      panel({ width: fill, height: hug, fill: "#1F2937", borderRadius: 10, padding: { x: 18, y: 16 } },
        text("Looks strong to the meter. Still follows a pattern.", { width: fill, height: hug, style: { fontSize: 23, color: "#D1D5DB" } })),
    ])),
]), notes[0]);

// 2
addSlide(column({ width: fill, height: fill, gap: 34, justify: "center" }, [
  label("Problem"),
  title("Password meters can reward surface complexity."),
  subtitle("A high score often reflects estimated guessing difficulty, but attackers can exploit predictable templates."),
  row({ width: fill, height: hug, gap: 70 }, [
    metric("length", "often increases score", C.blue),
    metric("symbols", "look complex", C.teal),
    metric("years", "can hide in templates", C.orange),
  ]),
]), notes[1]);

// 3
addSlide(grid({ width: fill, height: fill, columns: [fr(0.95), fr(1.05)], columnGap: 62, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 22 }, [
    label("Scoring Algorithm"),
    title("zxcvbn estimates guesses, not true randomness.", 52),
    subtitle("It detects patterns, estimates attack cost, and compresses that estimate into a 0-4 score."),
  ]),
  column({ width: fill, height: hug, gap: 20 }, [
    bullet("Pattern matching", "Dictionary words, dates, repeats, keyboard walks, and sequences."),
    bullet("Entropy estimate", "Combines detected chunks into an estimated number of guesses."),
    bullet("Adversarial gap", "Long predictable templates can still produce a high estimate."),
  ]),
]), notes[2]);

// 4
addSlide(grid({ width: fill, height: fill, columns: [fr(1), fr(1)], columnGap: 60, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 22 }, [
    label("Research Question"),
    title("Can ML generate meter-fooling passwords that remain crackable?", 52),
    subtitle("We test whether a model can learn high-scoring password patterns without learning true randomness."),
  ]),
  column({ width: fill, height: hug, gap: 20 }, [
    bullet("Generation script", "Produces passwords filtered by zxcvbn score 4."),
    bullet("Trained ML model", "Qwen2-0.5B fine-tuned with LoRA adapters."),
    bullet("10,000+ dataset", "Final merged set contains 19,574 unique generated passwords."),
  ]),
]), notes[3]);

// 5
addSlide(column({ width: fill, height: fill, gap: 30, justify: "center" }, [
  label("Dataset Construction"),
  title("We start weak, then add predictable complexity.", 52),
  grid({ width: fill, height: hug, columns: [fr(1), fr(1), fr(1), fr(1)], columnGap: 16 }, [
    step("root", "common passwords", "short, leaked, guessable roots"),
    step("+", "season words", "spring, summer, fall, winter"),
    step("+", "years", "1990 through 2025"),
    step("+", "symbols", "@, !, #, underscore"),
  ]),
  panel({ width: fill, height: hug, fill: C.dark, borderRadius: 12, padding: { x: 24, y: 18 } },
    text("Example template: admin + 1997 + ! + spring → admin1997!spring!", { width: fill, height: hug, style: { fontSize: 28, bold: true, color: C.white } })),
]), notes[4]);

// 6
addSlide(column({ width: fill, height: fill, gap: 32, justify: "center" }, [
  label("Pipeline"),
  title("Weak roots become high-score adversarial outputs.", 52),
  grid({ width: fill, height: hug, columns: [fr(1), fr(1), fr(1), fr(1), fr(1)], columnGap: 14 }, [
    step("1", "Clean", "filter raw common passwords"),
    step("2", "Modify", "add rule-based templates"),
    step("3", "Score", "keep zxcvbn 4/4 examples"),
    step("4", "Train", "fine-tune Qwen with LoRA"),
    step("5", "Generate", "filter and analyze outputs"),
  ]),
  subtitle("The model learns the distribution of passwords that pass the meter."),
]), notes[5]);

// 7
addSlide(grid({ width: fill, height: fill, columns: [fr(0.95), fr(1.05)], columnGap: 60, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 22 }, [
    label("Model"),
    title("Qwen2-0.5B + LoRA keeps the ML piece practical.", 52),
    subtitle("LoRA trains small adapter weights instead of retraining the full model."),
  ]),
  column({ width: fill, height: hug, gap: 20 }, [
    bullet("Base model", "Qwen/Qwen2-0.5B causal language model."),
    bullet("Training format", "Instruction-response JSONL: prompt in, password out."),
    bullet("Generation loop", "Sample candidates, clean outputs, keep zxcvbn score 4."),
  ]),
]), notes[6]);

// 8
addSlide(column({ width: fill, height: fill, gap: 38, justify: "center" }, [
  label("Result"),
  title("The generated dataset satisfies the core deliverable.", 52),
  row({ width: fill, height: hug, gap: 70 }, [
    metric("19,574", "unique generated passwords", C.blue),
    metric("100%", "score 4/4 on zxcvbn", C.teal),
    metric("16.5", "average length", C.orange),
  ]),
  panel({ width: fill, height: hug, fill: C.dark, borderRadius: 14, padding: { x: 28, y: 22 } },
    row({ width: fill, gap: 30 }, [
      text("@2021userfall", { width: fill, style: { fontSize: 30, bold: true, color: C.white } }),
      text("admin1997!spring!", { width: fill, style: { fontSize: 30, bold: true, color: C.white } }),
      text("#2015springfalluser", { width: fill, style: { fontSize: 30, bold: true, color: C.white } }),
    ])),
]), notes[7]);

// 9
addSlide(column({ width: fill, height: fill, gap: 22 }, [
  label("Weakness Evidence"),
  title("High-scoring does not mean random.", 52),
  subtitle("Most generated passwords contain targeted-rule ingredients."),
  column({ width: fill, height: hug, gap: 12 }, [
    bar("Contains year-like value", 0.992, "19,411 passwords", C.blue),
    bar("Contains a season", 0.845, "16,542 passwords", C.teal),
    bar("Contains a symbol", 0.967, "18,921 passwords", C.orange),
    bar("Contains both season and year", 0.838, "16,395 passwords", C.red),
  ]),
]), notes[8]);

// 10
addSlide(grid({ width: fill, height: fill, columns: [fr(0.95), fr(1.05)], columnGap: 60, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 20 }, [
    label("Attack Simulation"),
    title("A simple targeted rule set recovers real outputs.", 52),
    subtitle("Using only 100 common roots plus seasons, years, and symbols."),
  ]),
  column({ width: fill, height: hug, gap: 24 }, [
    metric("488,448", "rule guesses generated", C.blue, 44),
    metric("2,808", "generated passwords recovered", C.red, 44),
    metric("14.3%", "of the dataset recovered", C.teal, 44),
  ]),
]), notes[9]);

// 11
addSlide(column({ width: fill, height: fill, gap: 26, justify: "center" }, [
  label("Baseline Comparison"),
  title("Generated passwords score like random ones, but pattern like weak ones.", 48),
  table(["Dataset", "Avg score", "Score 4/4", "Avg length", "Season + year"], [
    ["Common weak", "0.01/4", "0.0%", "6.4", "0.0%"],
    ["Generated adversarial", "4.00/4", "100.0%", "16.4", "81.3%"],
    ["Random baseline", "4.00/4", "100.0%", "16.0", "0.0%"],
  ]),
  subtitle("The key distinction is not score. It is predictable structure."),
]), notes[10]);

// 12
addSlide(grid({ width: fill, height: fill, columns: [fr(1), fr(1)], columnGap: 60, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 22 }, [
    label("Live Demo"),
    title("The Flask app is a simple password lab.", 52),
    subtitle("It is designed to be usable, not report-like."),
  ]),
  column({ width: fill, height: hug, gap: 20 }, [
    bullet("Check a password", "Show zxcvbn score and detected features."),
    bullet("Generate 5", "Instant pattern-based demo outputs."),
    bullet("Show evidence", "Attack simulation, baseline table, samples, and CSV download."),
  ]),
]), notes[11]);

// 13
addSlide(grid({ width: fill, height: fill, columns: [fr(1), fr(1)], columnGap: 60, alignItems: "center" }, [
  column({ width: fill, height: hug, gap: 22 }, [
    label("Conclusion"),
    title("A high meter score is not the same as targeted-attack resistance.", 50),
    subtitle("The project demonstrates a practical gap between meter scoring and predictable password generation."),
  ]),
  column({ width: fill, height: hug, gap: 20 }, [
    bullet("Limitations", "Mostly zxcvbn; no full Hashcat benchmark yet."),
    bullet("Future work", "Test more meters and run real cracking experiments."),
    bullet("Takeaway", "Meters help, but they should not be treated as proof of true randomness."),
  ]),
]), notes[12]);

const pptxBlob = await PresentationFile.exportPptx(presentation);
await pptxBlob.save(path.join(outDir, "adversarial_password_meters_detailed.pptx"));

for (let i = 0; i < presentation.slides.count; i += 1) {
  const slide = presentation.slides.getItem(i);
  const png = await presentation.export({ slide, format: "png" });
  await fs.writeFile(path.join(outDir, `detailed-slide-${String(i + 1).padStart(2, "0")}.png`), Buffer.from(await png.arrayBuffer()));
}

await fs.writeFile(path.join(outDir, "speaker_notes.txt"), notes.map((n, i) => `Slide ${i + 1}\n${n}\n`).join("\n"));

console.log(`Exported ${presentation.slides.count} detailed slides with speaker notes to ${outDir}`);
