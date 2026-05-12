# Experiment: Vyhodnocení promptů — generování a hodnocení příkladů kognitivních zkreslení

**Cíl:** Porovnat kvalitu promptů pro generování příkladů kognitivních zkreslení (M1)
a jejich LLM hodnocení (M2) napříč různými modely. Výsledkem jsou podklady pro ADR-003
(výběr LLM pro produkci) a zlatá sada příkladů jako few-shot materiál pro v2 prompty.

Viz `GENERATION_CONCEPT.md` pro celkovou architekturu LLM použití v projektu.

---

## Struktura adresáře

```
experiments/2026-05-prompt-evaluation/
├── README.md               ← tento soubor — přehled a navigace
├── GENERATION_CONCEPT.md   ← architekturní rozhodnutí (online/offline LLM, en-general)
├── MANUAL_WORKFLOW.md      ← postup pro ruční spouštění modelů bez API
│
├── src/                    ← nástroje (nemění se mezi experimenty)
│   ├── pipeline.py         ← ALG1: gen/eval/report subpříkazy
│   ├── eval.py             ← eval.py: generování + hodnocení v jednom průchodu
│   └── requirements.txt    ← Python závislosti
│
└── data/
    ├── curated/            ← manuálně schválené příklady jako few-shot materiál
    │   ├── good/           ← příklady připravené k použití (řazeno dle typu zkreslení)
    │   └── borderline/     ← příklady vyžadující úpravu před použitím
    │
    ├── v1-plain/           ← experiment v1: základní prompty bez few-shot příkladů
    │   ├── README.md       ← datum, modely, závěry
    │   ├── prompts/        ← přesně ty prompty, které běžely v tomto experimentu
    │   └── results/        ← surová data, hodnocení, reporty
    │
    └── v2-fewshot/         ← (plánováno) experiment v2: prompty s few-shot příklady
```

---

## Instalace

```bash
cd experiments/2026-05-prompt-evaluation

# Vytvoř virtuální prostředí
python3 -m venv .venv
source .venv/bin/activate

# Nainstaluj závislosti
pip install -r src/requirements.txt
```

## API klíče

Klíče se načítají z `.env` souboru v kořeni projektu (nebo z proměnných prostředí).
Nikdy se necommitují do gitu.

```bash
# .env v kořeni projektu (viz .env.example):
OPENAI_API_KEY="sk-..."          # Povinný pro gpt-4o-mini a další OpenAI modely
GOOGLE_API_KEY="AI..."           # Volitelný — Gemini (free tier dostupný)
ANTHROPIC_API_KEY="sk-ant-..."   # Volitelný — Claude modely
```

| Poskytovatel | URL | Free tier? |
|---|---|---|
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | Ne — nutné dobití |
| Google | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Ano — Gemini Flash zdarma |
| Anthropic | [console.anthropic.com](https://console.anthropic.com) | Ne — nutné dobití |

---

## Spuštění (pipeline.py — ALG1)

```bash
# Generování příkladů modelem M1
python src/pipeline.py gen --model gpt-4o-mini

# Hodnocení výstupu M1 modelem M2
python src/pipeline.py eval --gen-model gpt-4o-mini --eval-model gpt-4o

# Vygenerování HTML reportu (tabulka M1 × M2)
python src/pipeline.py report

# Výpis dostupných modelů a jejich stavu
python src/pipeline.py models

# Výpis nalezených gen/eval souborů
python src/pipeline.py list
```

Aktivní run se nastavuje konstantou `_RUN_NAME` v `src/pipeline.py` (výchozí: `v1-plain`).

## Spuštění (eval.py — průběžné testování)

```bash
# Základní spuštění: gpt-4o-mini, 2 varianty na zkreslení, anglicky
python src/eval.py

# Porovnání dvou modelů, 3 varianty, česky
python src/eval.py --models gpt-4o-mini,gemini-2.0-flash --variants 3 --lang cs

# Rychlý test: jedno zkreslení, jedna varianta
python src/eval.py --bias anchoring --variants 1

# Všechny volby
python src/eval.py --help
```

Výstupy `eval.py` se ukládají do `data/eval-runs/<YYYYMMDD_HHMMSS>_<git-hash>/`.

---

## Bodovací rubrika (manuální přepsání)

Po přečtení `report.md` lze do `summary.json` ručně doplnit `human_score`:

| Skóre | Význam |
|---|---|
| 1.0 | Perfektní — lze použít přímo v produkci |
| 0.8 | Dobré — drobná úprava formulace |
| 0.6 | Hraničně — použitelné, ale suboptimální |
| 0.4 | Slabé — vyžaduje přepracování |
| 0.0–0.3 | Zamítnout — špatné zkreslení nebo zavádějící |

---

## Odhadované náklady

| Scénář | API volání | Odhadované náklady |
|---|---|---|
| 1 model, 5 zkreslení, 2 varianty | 20 | ~$0.01 |
| 2 modely, 5 zkreslení, 3 varianty | 60 | ~$0.03 |
| 3 modely, 5 zkreslení, 3 varianty | 90 | ~$0.04 |

---

## Kritéria rozhodnutí (kdy finalizovat ADR-003)

Po otestování ≥ 3 variant na zkreslení na model:

- **judge_pass ≥ 80 %** → model je přijatelný
- **Průměrné judge_score ≥ 0.75** → kvalita je dobrá
- **Subjektivní hodnocení** kvality češtiny (spusť s `--lang cs`)

Výsledek zapiš do `doc/architecture/decisions/ADR-003-llm-provider.md`
(Epic E030, task T010).
