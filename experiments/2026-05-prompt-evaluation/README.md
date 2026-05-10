# Experiment: Prompt Evaluation — Case Generation + Judge

**Goal:** Evaluate the quality of cognitive bias Case generation and LLM-as-judge
validation prompts across multiple LLM models, before wiring them into production code
(Epic E030, T020 + T040).

**Outcome:** Choose the best model for ADR-003; confirm that prompts produce valid,
educationally sound Cases.

---

## Setup

```bash
cd experiments/2026-05-prompt-evaluation

# Create a venv (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## API keys

Set keys for the providers you want to test. Keys are never committed to git.

```bash
export OPENAI_API_KEY="sk-..."          # Required for gpt-4o-mini
export GOOGLE_API_KEY="AI..."           # Optional — Gemini (free tier available)
export ANTHROPIC_API_KEY="sk-ant-..."   # Optional — Claude Haiku/Sonnet
```

Models skipped silently if their key is absent.

### Where to get each key

| Provider | URL | Free tier? |
|----------|-----|-----------|
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | No — needs billing ($5 credit lasts ~5 000 runs) |
| Google | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Yes — Gemini Flash is free with rate limits |
| Anthropic | [console.anthropic.com](https://console.anthropic.com) | No — needs billing |

---

## Prompt files

Prompts live in `prompts/prompts-v<VERSION>.json`. Both the generator and judge prompt
are in one file (they belong together). To iterate on prompts, create a new version file —
never edit an existing one.

```bash
# List available prompt versions
python eval.py --list-prompts

# Create a new prompt version by copying the latest:
cp prompts/prompts-v1.0.0.json prompts/prompts-v1.1.0.json
# ... edit prompts-v1.1.0.json ...
# Next run will auto-select v1.1.0 as the highest version
```

Each run output directory contains a **copy** of the prompt file used, so results
are always reproducible even after the prompt file changes.

## Usage

```bash
# Minimal: GPT-4o-mini only, 2 variants per bias, English output (uses latest prompts)
python eval.py

# Compare two models, 3 variants, Czech output
python eval.py --models gpt-4o-mini,gemini-2.0-flash --variants 3 --lang cs

# Quick test: one bias type, one variant
python eval.py --bias anchoring --variants 1

# Use a specific prompt version
python eval.py --prompt-version 1.0.0

# All options
python eval.py --help
```

---

## Output structure

Each run creates a directory:

```
data/prompt-eval/
└── 20260510_143022_a1b2c3d/      ← YYYYMMDD_HHMMSS_<git-hash>
    ├── run_meta.json              ← models, bias types, git state, prompt version
    ├── prompts-v1.0.0.json        ← copy of the prompt file used (reproducibility)
    ├── raw/
    │   ├── gpt-4o-mini/
    │   │   ├── anchoring_v0_gen.json    ← raw API response for generation
    │   │   ├── anchoring_v0_judge.json  ← raw API response for judge
    │   │   ├── anchoring_v1_gen.json
    │   │   └── ...
    │   └── gemini-2.0-flash/
    │       └── ...
    ├── report.md                  ← human-readable case-by-case comparison
    └── summary.json               ← scores + costs only (for cross-run comparison)
```

`data/` is committed to git — results are preserved as part of the repository.

---

## How to read the report

`report.md` contains one section per bias type, with each model/variant rendered as:

```
### `gpt-4o-mini` | variant 1  ✅  score=0.88

**The salary anchoring trap**

> Your manager mentions the team's average salary is 65 000 Kč/month before
> your review. You feel your request for 72 000 Kč is bold, even though market
> data suggests 80 000 Kč. What should you do?

- **A**: Accept 72 000 Kč as a fair compromise
- **B**: Ignore the stated average and research market rates independently  ✅
- **C**: Ask for 65 000 Kč to avoid conflict
- **D**: Postpone the discussion to next quarter

*Explanation:* The manager's stated average is an anchor that distorts your
perception of a fair salary. Researching independent market data removes the
anchor's influence and lets you negotiate based on actual value.

**Judge:** Strong anchoring scenario; all distractors believable; explanation clear.
**Cost:** $0.00042
```

---

## Scoring rubric (manual override)

After reviewing `report.md`, add a `human_score` column to `summary.json` manually
if the judge score does not match your assessment. Use this to detect systematic
over/under-scoring by the judge prompt itself.

| Score | Meaning |
|-------|---------|
| 1.0 | Perfect — would use this Case as-is in production |
| 0.8 | Good — minor rewording needed |
| 0.6 | Borderline — usable but clearly suboptimal |
| 0.4 | Weak — would need significant rework |
| 0.0–0.3 | Reject — wrong bias or misleading |

---

## Estimated costs

| Scenario | API calls | Estimated cost |
|----------|-----------|---------------|
| 1 model, 5 biases, 2 variants | 20 | ~$0.01 |
| 2 models, 5 biases, 3 variants | 60 | ~$0.03 |
| 3 models, 5 biases, 3 variants | 90 | ~$0.04 |

---

## Decision criteria (when to finalize ADR-003)

After testing ≥ 3 variants per bias per model:

- **judge_pass rate ≥ 80 %** → model is acceptable
- **Average judge_score ≥ 0.75** → model quality is good
- **Your subjective assessment** of Czech language quality (run with `--lang cs`)

Document the winning model choice in `doc/architecture/decisions/ADR-003-llm-provider.md`
(E030 T010) and proceed with Epic E030.
