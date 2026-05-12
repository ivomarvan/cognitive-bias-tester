# Manuální workflow pro modely bez API přístupu

Modely jako **Claude Opus 4.7**, **GPT-5.5**, **Gemini 3.1 Pro** nelze (nebo není vhodné)
spouštět přes API kvůli ceně nebo dostupnosti. Výsledné JSON soubory ale lze do matice
přidat ručně — `pipeline.py report` je automaticky zahrne.

---

## Konvence souborů

```
data/example-eval/
├── gen/<model-slug>.json             ← json1: výstup generačního kroku
└── eval/<gen-slug>__by__<eval-slug>.json  ← json2: výstup evaluačního kroku
```

**Model slug** = zjednodušený identifikátor bez mezer a lomítek, malá písmena:

| Model | Slug |
|-------|------|
| Claude Opus 4.7 | `claude-opus-4-7` |
| GPT-5.5 | `gpt-5.5` |
| Gemini 3.1 Pro | `gemini-3.1-pro` |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` |

---

## Krok 1 — Generace (json1)

### 1a. Připrav prompt

Obsah souboru:
```
experiments/2026-05-prompt-evaluation/prompts/author/prompt_for_examples.md
```

### 1b. Spusť v rozhraní modelu

- Otevři rozhraní modelu (claude.ai, chat.openai.com, aistudio.google.com...)
- Vlož **celý obsah** `prompt_for_examples.md` jako zprávu
- Počkej na výstup (může trvat 1–3 minuty)
- Model by měl vrátit čistý JSON (bez markdown fences)

> **Pokud model vrátí JSON obalený v ```json ... ```:**
> Smaž fences ručně, nebo přidej instrukci do zprávy:
> "Vrať pouze čistý JSON bez markdown formatování."

### 1c. Ulož výstup

Zkopíruj výsledný JSON do souboru:
```
data/example-eval/gen/<model-slug>.json
```

Příklad:
```
data/example-eval/gen/claude-opus-4-7.json
```

### 1d. Ověř JSON

```bash
python3 -c "import json; d=json.load(open('data/example-eval/gen/claude-opus-4-7.json')); print('OK, biases:', [k for k in d if k!='_metadata'])"
```

Očekávaný výstup:
```
OK, biases: ['anchoring', 'framing', 'loss_aversion', 'confirmation_bias', 'sunk_cost_fallacy']
```

---

## Krok 2 — Evaluace (json2)

### 2a. Připrav zprávu

Sestav zprávu ze dvou částí:

**Část 1 — System prompt:**
Celý obsah souboru:
```
experiments/2026-05-prompt-evaluation/prompts/author/prompt_for_evaluating_generated_examples.md
```

**Část 2 — User message:**
```
# Vstup

Zdrojový soubor: <model-slug>.json

<celý obsah json1 souboru>
```

> **Tip:** V rozhraních podporujících system prompt (Claude, ChatGPT s projekty)
> použij system slot pro evaluační instrukce a user slot pro json1.
> V rozhraních bez system promptu vlož oboje do jedné zprávy.

### 2b. Spusť v rozhraní modelu M2

- Vlož zprávu do rozhraní evaluátorského modelu
- Model by měl vrátit čistý JSON s hodnocením

### 2c. Ulož výstup

```
data/example-eval/eval/<gen-slug>__by__<eval-slug>.json
```

Příklad (Opus 4.7 generoval, GPT-5.5 hodnotil):
```
data/example-eval/eval/claude-opus-4-7__by__gpt-5.5.json
```

### 2d. Ověř JSON

```bash
python3 -c "
import json
d = json.load(open('data/example-eval/eval/claude-opus-4-7__by__gpt-5.5.json'))
s = d.get('statistics', {})
print('Score:', s.get('overall_mean_weighted'))
print('Flagged:', len(s.get('flagged_examples', [])))
"
```

---

## Krok 3 — Aktualizuj report

Po každém přidaném souboru spusť:

```bash
cd experiments/2026-05-prompt-evaluation
python pipeline.py report
```

Otevři `data/example-eval/report.html` v prohlížeči.

---

## Doporučené pořadí pro první kolo

### Generace (M1)

| Pořadí | Model | Přístup | Příkaz / akce |
|--------|-------|---------|---------------|
| 1 | gpt-4o-mini | API | `python pipeline.py gen --model gpt-4o-mini` |
| 2 | gemini-2.0-flash | API | `python pipeline.py gen --model gemini-2.0-flash` |
| 3 | claude-3-5-haiku | API | `python pipeline.py gen --model claude-3-5-haiku-20241022` |
| 4 | claude-opus-4-7 | manuál | viz postup výše |
| 5 | gpt-5.5 | manuál | viz postup výše |

### Evaluace (M2) — minimální matice

| M1 | M2 | Přístup | Příkaz / akce |
|----|-----|---------|---------------|
| gpt-4o-mini | gpt-4o | API | `python pipeline.py eval --gen-model gpt-4o-mini --eval-model gpt-4o` |
| gpt-4o-mini | gemini-2.5-pro | API | `python pipeline.py eval --gen-model gpt-4o-mini --eval-model gemini-2.5-pro` |
| gemini-2.0-flash | gpt-4o | API | `python pipeline.py eval --gen-model gemini-2.0-flash --eval-model gpt-4o` |
| claude-3-5-haiku | gpt-4o | API | `python pipeline.py eval --gen-model claude-3-5-haiku-20241022 --eval-model gpt-4o` |
| claude-opus-4-7 | gemini-2.5-pro | API | `python pipeline.py eval --gen-model claude-opus-4-7 --eval-model gemini-2.5-pro` |
| claude-opus-4-7 | gpt-5.5 | manuál | viz postup výše |
| gpt-5.5 | claude-opus-4-7 | manuál | viz postup výše |

---

## Troubleshooting

**Model vrátil zkrácený JSON (chybí závěrečné `}`)**

Velký výstup (40 příkladů) může přesáhnout output limit. Zkus:
1. Požádat o kratší výstup: "Vygeneruj pouze pro `anchoring` a `framing`"
2. Spustit ve dvou kolech a ručně sloučit JSON

**Evaluátor vrátil jiný formát než očekávaný**

Zkontroluj, zda `_metadata`, `evaluation_results` a `statistics` jsou přítomny.
Pokud ne, můžeš přidat prázdné kostry ručně — report.py je tolerantní vůči chybějícím polím.

**pipeline.py report nezobrazuje ručně vložený soubor**

Zkontroluj název souboru — musí přesně odpovídat formátu `<gen-slug>__by__<eval-slug>.json`
(dvě podtržítka na každé straně `by`).
