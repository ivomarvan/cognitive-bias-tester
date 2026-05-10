# Task: Create Gold-Standard Few-Shot Examples for Cognitive Bias Cases

## Your role

You are an expert in cognitive psychology, behavioural economics, and educational content
design. You are creating **gold-standard example Cases** that will be embedded in AI prompts
as few-shot demonstrations. Their quality directly determines the quality of all
subsequently generated Cases in a production system.

This is not a creative exercise — it is precision work. Every Case will be scrutinized
by an independent validator. Aim for the best you can possibly produce.

---

## Output language

**Czech (čeština).** All `title`, `question`, `options.text`, and `explanation` fields
must be in natural, contemporary Czech. The JSON keys remain in English.

---

## Output format

Produce **exactly 5 JSON objects** — one per bias type listed below.
Output them as a JSON array. No markdown fences, no commentary outside the array.

Required schema per Case:
```json
{
  "bias_type_slug": "string — one of the 5 slugs below",
  "title": "string — short scenario title, max 10 Czech words",
  "question": "string — realistic scenario (3–5 sentences) + question for the user",
  "options": [
    {"label": "A", "text": "string — answer option in Czech"},
    {"label": "B", "text": "string — answer option in Czech"},
    {"label": "C", "text": "string — answer option in Czech"},
    {"label": "D", "text": "string — answer option in Czech"}
  ],
  "correct_option": 0,
  "explanation": "string — 3–4 sentences in Czech: what bias occurred, why the correct option avoids it, what the rational approach is",
  "parametric_payload": {}
}
```

---

## The 5 bias types

### 1. `anchoring` — Ukotvení

**Definition:** The first piece of numerical information presented (the "anchor") exerts
a disproportionate influence on all subsequent estimates and decisions, even when the
anchor is arbitrary or irrelevant.

**Structural requirement:** The scenario MUST present an explicit number, price, or
quantity as the first reference point. The irrational behaviour consists of being pulled
toward this anchor instead of using independent reasoning or data.

**Classic patterns:** salary negotiation starting from an arbitrary figure; a product's
"original price" making the sale price feel like a bargain; a doctor's initial estimate
biasing a patient's expectations.

---

### 2. `framing` — Rámování

**Definition:** The same objective fact or choice leads to different decisions depending
on how it is presented — as a gain, a loss, a percentage, or an absolute number.

**Structural requirement:** The scenario MUST present TWO or more options that are
logically equivalent but framed differently. The irrational behaviour is choosing based
on the frame rather than the underlying reality.

**Classic patterns:** "90% survival rate" vs. "10% mortality rate"; "saves 200 lives"
vs. "400 will die"; "contains 10% fat" vs. "90% fat-free"; a politician describing
unemployment as "3% jobless" vs. "97% employed".

---

### 3. `loss_aversion` — Averze ke ztrátě

**Definition:** Losses feel psychologically approximately twice as powerful as
equivalent gains. This causes people to take irrational risks to avoid losses or to
irrationally avoid risks that could produce gains.

**Structural requirement:** The scenario MUST frame a choice explicitly in terms of
potential loss on one side and potential gain on the other, where the expected values
are equal or the rational choice is the "gain" option but the person irrationally
chooses the "loss avoidance" path.

**Classic patterns:** refusing a 50/50 bet because the potential loss feels worse than
the equivalent potential gain; holding a losing stock because selling "feels like"
accepting a loss; paying for extended warranty on a cheap appliance.

---

### 4. `confirmation_bias` — Konfirmační zkreslení

**Definition:** The tendency to search for, interpret, favour, and recall information
that confirms one's pre-existing beliefs, while ignoring contradicting evidence.

**Structural requirement:** The scenario MUST show a character who already holds a
belief and then faces new information. The irrational behaviour is selectively accepting
confirming evidence and dismissing (or not seeking) disconfirming evidence.

**Classic patterns:** a manager who has decided on a candidate reads their CV looking
for strengths only; an investor who believes in a stock ignores negative analyst reports;
someone self-diagnosing a serious illness via search engine and only clicking confirming
results.

---

### 5. `sunk_cost_fallacy` — Klam utopených nákladů

**Definition:** Continuing a failing course of action because of previously invested
resources (money, time, effort) that cannot be recovered, rather than evaluating only
future costs and benefits.

**Structural requirement:** The scenario MUST make clear that a cost has already been
paid and is irrecoverable. The irrational behaviour is letting that past investment
drive the future decision instead of evaluating what makes sense going forward.

**Classic patterns:** finishing a terrible book because you paid for it; continuing a
failing project because the team has spent 2 years on it; staying in a career you
dislike because you paid for the degree; eating bad restaurant food because it was
expensive.

---

## Quality criteria (each Case will be validated against these)

| Criterion | Requirement |
|-----------|-------------|
| **Bias purity** | The scenario demonstrates exactly the specified bias — no other bias is a plausible explanation |
| **Realistic scenario** | Could happen to a contemporary Czech adult; not a textbook abstraction |
| **Option plausibility** | All 4 options must be plausible responses; no obviously "dumb" distractors |
| **Correct option clarity** | The correct option is rational and defensible, but not trivially obvious |
| **correct_option distribution** | Do NOT use index 0 or 1 for all 5 cases — distribute across 0, 1, 2, 3 |
| **Explanation depth** | Names the bias, explains the mechanism, describes the rational alternative |
| **Czech language** | Natural, contemporary Czech; no overly formal or translated feel |
| **Difficulty calibration** | Should make a thoughtful adult pause — not a puzzle for a psychologist |

---

## Anti-patterns to avoid

- ❌ Scenarios that are too abstract ("Imagine you have invested $X...")
- ❌ Options where one is obviously a joke or socially unacceptable
- ❌ Explanation that only says "because of the bias" without explaining the mechanism
- ❌ Scenarios where multiple biases apply equally well
- ❌ Using the word "zkreslení/bias" in the scenario text itself
- ❌ Identical scenario structure across different bias types

---

## Output

Produce the 5 Cases as a single JSON array. Start with `[` and end with `]`.
No other text before or after.
