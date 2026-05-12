# Concept: LLM Usage for Cognitive Bias Tester

*Working document — will be updated as prompt experiments progress.*
*Detailed APM plan will follow once prompts are finalized.*

---

## 1. Two Modes of LLM Usage

### 1.1 Online (Realtime)

Used for **translations only** — both UI strings and bias examples for new languages.

- Triggered on-demand when a user's locale is not yet cached.
- Runs in the background; result is cached immediately.
- Model: cheaper, fast model (e.g., GPT-4o-mini or Gemini Flash).
  - **Must be validated** for mathematical correctness before production deployment
    (cheap models failed generation but may suffice for translation with explicit rules).
- Cache invalidation: via `source_hash` (SHA-256 of source string + `translation_context`),
  already defined in the i18n spec from E020.

### 1.2 Offline (Batch)

Used for **generating new bias examples**. Runs periodically, not on user request.

- Runs as a backend tool (script / CLI) — operators control when and how much to generate.
- **Controlled cost**: generate N examples per run, review quality, insert into DB.
- Model: strong model (Claude Sonnet 4.6 or GPT-5.5 for routine runs; Opus 4.7 for high-quality batches).
- Output goes through quality review before DB insertion (automated score + optional manual).

---

## 2. Example Schema: `en-general` as Source of Truth

### 2.1 Concept

All bias examples are stored in DB in a neutral **`en-general`** form:
- Canonical English text with **placeholder variables** for locale-sensitive values.
- Accompanied by `translation_context` that defines rules for translators.

When rendering for a user:
1. Check cache: is there a localized version for this `(example_id, locale)`?
2. If yes → use cached version.
3. If no → call translation LLM with `(en-general text + translation_context + target_locale)`.
4. Validate result (at minimum: check mathematical invariants programmatically).
5. Cache and return.

English users also receive a translated version (en-general → en) — ensures consistent localization pipeline for all locales.

### 2.2 Placeholder Format

```json
{
  "question": "You are offered a single bet: a coin flip pays {{gain_amount}} if heads, loses {{loss_amount}} if tails.",
  "translation_context": {
    "summary": "Loss aversion trap: EV = 0.5×gain − 0.5×loss is positive. Biased answer avoids the bet due to loss pain.",
    "values": {
      "gain_amount": {
        "canonical": 150,
        "currency": "EUR",
        "rule": "Psychologically round number in target currency. Example: 3 000 Kč, 150 €, $150."
      },
      "loss_amount": {
        "canonical": 100,
        "currency": "EUR",
        "rule": "Approximately 2/3 of gain_amount, rounded. Must be < gain_amount."
      },
      "ev_result": {
        "canonical": 25,
        "currency": "EUR",
        "rule": "Recalculate: 0.5 × translated(gain_amount) − 0.5 × translated(loss_amount). Show in rational explanation."
      }
    },
    "invariants": [
      "EV = 0.5×gain_amount − 0.5×loss_amount MUST be positive (gain_amount > loss_amount)",
      "loss_amount < gain_amount",
      "ev_result in rational explanation must match the translated values"
    ]
  }
}
```

### 2.3 DB Schema Change (relative to E020)

Add column to `cases` table:
```sql
ALTER TABLE cases ADD COLUMN translation_context JSONB;
```

`language_code = 'en-general'` is a reserved value — stored once per example, never shown to users directly.

---

## 3. Prompt Architecture

### Prompt A — Single-Bias Generator

Generates examples for **one bias type** at a time. Returns:
- Array of 3–8 examples with placeholders and `translation_context`.
- Token count (requested explicitly in prompt for manual runs without API).
- Few-shot examples included for each bias type (from `selected_good_examples/`).

Stored at: `experiments/2026-05-prompt-evaluation/prompts/author/prompt_for_examples.md`
(will be updated to v2 with placeholders + few-shot + token request)

### Prompt B — Orchestrator (for manual runs)

For models without API access, Prompt B contains instructions to:
- Run Prompt A independently for each of the 5 bias types.
- Return merged JSON with all results.
- Include total token count for cost estimation.

For API runs: `pipeline.py gen --model <model>` already does this automatically (by-bias mode).

### Prompt V — Validator

Evaluates generated examples. Unchanged from v1.0.
Stored at: `experiments/2026-05-prompt-evaluation/prompts/author/prompt_for_evaluating_generated_examples.md`

---

## 4. Planned Experiment Steps (v2 prompt round)

| Step | Action | Model | Tool |
|------|--------|-------|------|
| a | Select few-shot examples from `selected_good_examples/` | Human | Manual review |
| b | Rewrite examples with `{{placeholders}}` and `translation_context` | Human | Editor |
| c | Update Prompt A: add few-shot + placeholder instructions + token count request | Human | Editor |
| d | Generate new examples | Sonnet 4.6, Gemini 3.1 Pro (API); Opus 4.7 optionally manual | `pipeline.py gen` |
| e | Evaluate with Sonnet 4.6 as judge + capture token count → cost estimate | Sonnet 4.6 | `pipeline.py eval` + `report` |
| f | Decision: select production model based on quality/cost ratio | Human | Report |
| g | Select best examples from all rounds → DB insertion tool | Human + Coder | New task in E030 |

---

## 5. Cost Estimates (per example generation, by-bias mode)

Rough: ~800 tokens input + ~500 tokens output per bias per call (5 calls = 1 full set of 40 examples).

| Model | Input $/M | Output $/M | Cost / 40 examples | Quality |
|-------|-----------|------------|---------------------|---------|
| Claude Opus 4.7 | ~$15 | ~$75 | ~$0.21 | ⭐⭐⭐⭐⭐ (85.7) |
| Claude Sonnet 4.6 | ~$3 | ~$15 | ~$0.04 | ⭐⭐⭐⭐ (83.4) |
| GPT-5.5 | ~$2 | ~$8 | ~$0.025 | ⭐⭐⭐⭐ (80.3) |
| GPT-4o-mini | ~$0.15 | ~$0.6 | ~$0.002 | ❌ unusable |

Production recommendation: **Sonnet 4.6** or **GPT-5.5** for routine generation.
Opus 4.7 for high-quality batch runs (e.g., once per new bias type introduction).

---

## 6. Translation Cost (online, per example per language)

One translation call: ~600 tokens input + ~400 tokens output.

| Model | Cost / example / language |
|-------|--------------------------|
| GPT-4o-mini | ~$0.0003 |
| Gemini Flash | ~$0.0001 |
| Sonnet 4.6 | ~$0.008 |

Even with 1 000 examples × 10 languages = 10 000 translations → GPT-4o-mini ≈ $3 total (one-time cache fill).

---

## 7. Open Decisions

| # | Question | Status |
|---|----------|--------|
| 1 | Does GPT-4o-mini produce mathematically correct translations with explicit `invariants`? | ❓ To test |
| 2 | Final production model for generation (Sonnet 4.6 vs GPT-5.5)? | ❓ After v2 prompt round |
| 3 | DB insertion tool: standalone script or part of E030? | ❓ Decide during E030 planning |
| 4 | `translation_context` generation: mandatory in prompt or optional? | ❓ Test complexity impact first |

---

## 8. Relationship to Roadmap

- **E030 (LLM Pipeline & Cache)**: will implement the online translation pipeline and the offline generation tool.
- **E020 (Data Model)**: already supports the `cases` + `options` schema; `translation_context` column to be added as a migration in E030.
- **E040+**: generation tooling and batch workflows are a later epic (h from user's proposal).
