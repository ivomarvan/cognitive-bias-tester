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

## Fáze 2: Roadmap k produkčním datům

Navazuje na dokončení ruční revize v `data/v1-plain/curated/human evaluation.md`.

### Krok 1 — Extrakce `selected/`

Ze souborů v `curated/good/` a `curated/borderline/` (dle pokynů v `human evaluation.md`)
vytvoříme soubory v `data/selected/` obsahující pouze aplikačně relevantní data:
`id`, `bias`, `source`, `domain`, `difficulty`, `question`, `options`.
Metadata hodnocení (`evaluation`, `selection`) se vynechají — jejich účel byl vyčerpán.
Soubory z `curated/interactive/` se do `selected/` nekopírují — čekají na implementaci UI.

### Krok 1.5 — Finalizace schématu: pole `global_explanation`

Před překladem se ustálí finální tvar JSON příkladu přidáním pole `global_explanation`.

**Proč teď:** databáze ani GUI ještě neexistují; v2 prompt bude generovat příklady přímo
do finálního schématu a zpětná migrace stovek souborů bude zbytečná.

**Obsah pole:**
- Sdílený kontext, výpočet nebo logická premisa platná pro všechny options (EV, ekvivalence rámce, klíčová podmínka…)
- Smí být `null` / prázdný řetězec pro příklady bez sdíleného výpočtu (typicky sunk cost, kvalitativní scénáře)
- Zobrazí se uživateli jako část reveal screenu — před nebo vedle option-specific explanation

**Výsledné schéma příkladu v `selected/`:**
```json
{
  "id": "loss_aversion-own-02",
  "bias": "loss_aversion",
  "domain": "sport",
  "difficulty": 3,
  "question": "...",
  "global_explanation": "Očekávaná hodnota varianty B: 0,6·80 000 + 0,4·35 000 = 62 000 €. Pevná varianta A: 50 000 €.",
  "options": [
    { "answer": "Variantu B — statisticky výhodnější.", "verdict": "rational",
      "explanation": "Volba respektuje vyšší EV varianty B." },
    { "answer": "Variantu A — jistých 50 000 € je bezpečnější.", "verdict": "biased",
      "explanation": "Strach z propadu na 35 000 € psychologicky převáží vyšší průměr. Jedná se o typ zkreslení: averze ke ztrátě." },
    { "answer": "Variantu A, dokud klub nedoloží historii.", "verdict": "neutral",
      "explanation": "Podmínění dodatečnými informacemi obchází dostupná čísla." }
  ]
}
```

**Postup migrace (automatický skript):**
1. Přidat `global_explanation: null` do všech souborů v `selected/`
2. LLM průchod (Composer 2): vyplnit `global_explanation` z existujících `explanation` textů, extrahovat sdílený výpočet
3. Ruční kontrola a zkrácení option-specific `explanation` (odebrat opakující se výpočet)

### Krok 2 — `selected_with_context.cs`

Kopie `selected/` rozšířená o lokalizační kontext pro češtinu:
instrukce pro překlad (formát čísel, měny, typografické konvence),
metadata o cílových jazycích a poznámky k obtížným případům.

### Krok 3 — `selected_with_context.gen_en`

Automaticky generovaná anglická verze ze `selected_with_context.cs`.
LLM přeloží příklady dle pravidel z kroku 2.
Tento adresář je artefakt — nepíše se ručně.

### Krok 4 — Zpětná validace překladů

Přeložené anglické příklady se kontrolně přeloží zpět do češtiny a porovnají s originálem.
Instrukce z kroku 2 se iterativně ladí, dokud zpětný překlad nedrží pedagogický záměr.

### Krok 5 — Nové prompty v2

Anglicky, few-shot příklady z kroku 4 jako ilustrace standardu.
Dva prompty: generování (zobecnění `prompt_for_examples.md`) a validace (zobecnění `prompt_for_evaluating_generated_examples.md`).
Oba prompty obsahují požadavek na odhad tokenů a zohledňují zkušenosti z formulace
příkladů — viz `data/formulation-insights.md`.
Výstup: `data/v2-fewshot/prompts/`.

### Krok 6 — Experiment v2-fewshot

Nové příklady generované v2 prompty s více modely.
Hodnocení kombinací generátor × hodnotitel.
Hypotéza: few-shot příklady + zohledněné zkušenosti umožní i slabším modelům generovat
příklady v produkční kvalitě. Výsledek ověříme.

### Krok 7 — Finální zlatá sada

Všechny příklady s hodnocením ≥ threshold z v1 i v2 se sloučí do `data/selected/`.
Tato sada je vstupní data pro vývoj aplikace (Epic E040+).

### Krok 8 — Archivace promptů

Odladěné v2 prompty se uloží jako základ offline nástroje pro průběžné generování
nových příkladů při rozšiřování zkreslení (E200, E210).

---

## Kritéria rozhodnutí (kdy finalizovat ADR-003)

Po otestování ≥ 3 variant na zkreslení na model:

- **judge_pass ≥ 80 %** → model je přijatelný
- **Průměrné judge_score ≥ 0.75** → kvalita je dobrá
- **Subjektivní hodnocení** kvality češtiny (spusť s `--lang cs`)

Výsledek zapiš do `doc/architecture/decisions/ADR-003-llm-provider.md`
(Epic E030, task T010).
