# Experiment v1-plain — základní prompty bez few-shot příkladů

**Datum:** květen 2026
**Stav:** dokončeno

---

## Cíl

Zjistit, které modely jsou vůbec schopné generovat kvalitní příklady kognitivních zkreslení
při použití základního promptu (bez few-shot příkladů, bez placeholderů).
Baseline pro porovnání s budoucími verzemi promptů.

## Použité modely

| Role | Modely |
|---|---|
| M1 (generování) | gpt-4o-mini, gpt-4o, gpt-5.5, gemini-3.1-pro, opus-4.7, sonnet-4.6 |
| M2 (hodnocení) | sonnet-4.6, gemini-3.1-pro |

## Závěry

- **GPT-4o-mini a GPT-4o selhaly** — logické chyby v racionalitě, záměna zkreslení
- **Opus 4.7 nejlepší kvalita** (průměr ~85 bodů) — správná struktura, čistá racionalita
- **Sonnet 4.6 a GPT-5.5 dobrý poměr cena/kvalita** — použitelné pro produkci
- Gemini 3.1 Pro hodnotí přísněji než Sonnet 4.6 (viz report.md — cross-evaluace)
- Sonnet 4.6 hodnotí sám sebe níže než Gemini 3.1 Pro — dobrý znak integrity

**Rozhodnutí pro produkci:** GPT-4o-mini nebo Sonnet 4.6 jako levný online model,
Opus 4.7 nebo GPT-5.5 pro offline batch generování. Viz `GENERATION_CONCEPT.md`.

---

## Struktura

```
v1-plain/
├── README.md               ← tento soubor
├── prompts/                ← přesně ty prompty, které se v tomto experimentu používaly
│   ├── prompt_for_examples.md                    ← generovací prompt (M1)
│   ├── prompt_for_evaluating_generated_examples.md  ← hodnotící prompt (M2)
│   ├── prompts-v1.0.0.json                       ← starší formát (eval.py)
│   └── tasks/              ← zadání pro manuální spuštění (bez API)
│       ├── task-create-gold-examples.cs.md
│       ├── task-create-gold-examples.en.md
│       ├── task-validate-gold-examples.cs.md
│       └── task-validate-gold-examples.en.md
└── results/
    ├── gen/                ← surové výstupy M1 (JSON soubory per model)
    ├── eval/               ← hodnocení M2 (JSON + .report.md per kombinaci M1×M2)
    ├── eval_script.py      ← skript použitý pro ruční hodnocení (gpt-4o-mini)
    ├── report.html         ← souhrnná tabulka M1 × M2
    └── report.md           ← textová verze reportu
```

## Kurátorský výstup

Nejlepší příklady z tohoto experimentu (generované Opus 4.7) byly ručně vybrány
a uloženy do `data/curated/` jako few-shot materiál pro experiment v2.

- `data/curated/good/` — příklady připravené k použití
- `data/curated/borderline/` — příklady vyžadující úpravu
