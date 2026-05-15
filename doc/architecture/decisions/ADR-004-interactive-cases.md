# ADR-004: Interaktivní Cases pro micro-interakce kognitivních zkreslení

**Stav**: Navrhováno
**Datum**: 2026-05-14

## Kontext

Všechny současné Case příklady jsou čistě textové (`case_type: "text"`). Uživatel přečte scénář a vybere jednu ze tří předepsaných odpovědí. Pro zkreslení jako je ukotvení je tato struktura pedagogicky slabá:

> Anchoring příklad „kola štěstí" (Kahneman & Tversky, 1974) funguje proto, že účastníci kolo opravdu
> roztočí — fyzicky prožijí náhodnou kotvu dříve, než je položena otázka. Text říkající
> *„kolo se zastavilo na čísle 65"* je zpracován jako **informace**, nikoli jako **zážitek**. Uživatel ho může
> vědomě kompenzovat, čímž celý smysl demonstrace zaniká.

Stejná strukturní slabina platí (v různé míře) pro každé podporované zkreslení.
**Interaktivní micro-interakce** — Vue komponenta předcházející otázce — může obnovit zážitkovou vrstvu,
která kognitivní past činí skutečnou.

## Rozhodnutí: Varianta A — lehká Vue komponenta pro každý typ Case

Do JSON schématu Case se zavádí volitelný blok `ui_hint`. Pokud je přítomen, frontend před zobrazením otázky
vykreslí příslušnou Vue komponentu. Komponenta spravuje vlastní stav, vytváří payload `anchor_context`
a emituje událost `done` pro odkrytí otázky.

**Rozšíření schématu:**

```json
{
  "example": {
    "ui_hint": {
      "case_type": "interactive",
      "component": "WheelOfFortune",
      "variant": "A",
      "anchor_value": 65,
      "anchor_range_low": [10, 25],
      "anchor_range_high": [60, 80],
      "randomize_anchor": true
    }
  }
}
```

`case_type` = `"text"` (výchozí, stávající chování) | `"interactive"` (vyžaduje komponentu).

**Pravidlo fallbacku**: Pokud komponentu nelze vykreslit (SSR, režim přístupnosti, žádný JS), Case se degraduje
na svou textovou verzi — otázka se zobrazí ihned bez pre-interakce.

## Implementace: komponenta WheelOfFortune (ukotvení)

**UX flow:**
1. Uživatel přijde na Case. Místo otázky vidí stylizované ruletové kolo s jasně viditelnými čísly: mix
   nízkých hodnot (10–25) a vysokých hodnot (60–80).
2. Uživatel klikne na **„Zatočit"**.
3. Přehraje se CSS `@keyframes` + zpomalení s `cubic-bezier` (≈ 3 s). Kolo není skutečně náhodné —
   vždy se zastaví na `anchor_value` (nebo pseudonáhodně z `anchor_range_high`), aby vznikla vysoká kotva.
   Příležitostně dostane ~30 % uživatelů variantu s nízkou kotvou pro A/B efekt.
4. Padlé číslo zůstane viditelné ve výrazném odznaku. Krátká pauza (500 ms), pak pod kolem přisvitne otázka.
5. Po odpovědi uživatele zobrazí reveal screen:
   - Distribuční sloupcový graf: *„Uživatelé, kteří dostali ~15, odhadovali průměrně 25 %;
     uživatelé s ~65 odhadovali průměrně 45 %."*
   - Značku s odpovědí uživatele.
   - Správnou odpověď (28 %).
   - Jednovětu vysvětlení: *„Náhodné číslo z kola ovlivnilo váš odhad — to je ukotvení."*

**Proč Varianta A (oproti alternativám):**
- Varianta B (statický GIF) odstraňuje interaktivitu — žádný pocit vlastní akce, slabší ponoření.
- Varianta C (plná pravděpodobnostní simulace) je pro MVP over-engineered; pedagogický přínos oproti A je malý.
- Varianta A má vysoký poměr přínosu ke složitosti: jedna samostatná Vue komponenta, žádné backendové
  změny, žádná migrace schématu (pole je additivní).

## Kandidáti na interaktivní Cases pro ostatní typy zkreslení

### Framing — reveal „Stejná data, dva rámce"

**Trigger**: `component: "FramingReveal"`

**UX flow:** Uživatel vidí Rámec A (*„200 z 600 pacientů přežije"*) a vybere možnost léčby.
Po odpovědi se vedle objeví Rámec B (*„400 z 600 pacientů zemře"*) — stejná data, jiná formulace.
Slider umožní odpovědět znovu s vědomím obou rámců. Rozdíl mezi první a druhou odpovědí je změřený
framing efekt.

**Pedagogická hodnota**: Vysoká. Uživatel v reálném čase pocítí vlastní nekonzistenci.

### Averze ke ztrátě — micro-hra „Sázka žetonů"

**Trigger**: `component: "TokenBet"`

**UX flow:** Uživatel začíná s 500 žetony. Jsou mu předloženy dvě volby:
  - *„Získejte jistých 100 žetonů"* vs. *„50% šance získat 250 žetonů"*
  - *„Prohrajte jistých 100 žetonů"* vs. *„50% šance prohrát 250 žetonů"*

Tři kola, očekávaná hodnota v každém páru identická. Po kolech následuje otázka Case.
Obrazovka výsledků ukáže: *„Většina lidí přijímá jistý zisk a odmítá jistou ztrátu — přestože
matematika je identická. Tato asymetrie je averze ke ztrátě."*

**Pedagogická hodnota**: Velmi vysoká. Vlastní volby uživatele se stávají důkazem.

### Konfirmační zkreslení — čtečka „Selektivní feed"

**Trigger**: `component: "SelectiveFeed"`

**UX flow:** Uživateli je předloženo tvrzení: *„Používání sociálních médií zvyšuje depresi u teenagerů."*
Níže: osm titulků článků (čtyři podporující, čtyři vyvracející), náhodně seřazené.
Uživatel klepne na **až pět** titulků a „přečte" je (zobrazí se krátký úryvek). Po čtení ohodnotí
svou důvěru v tvrzení (1–5). Výsledek ukáže, kolik pro/proti článků si vybral oproti tomu, co bylo dostupné.
Většina uživatelů přečte výrazně více podporujících článků.

**Pedagogická hodnota**: Vysoká. Vlastnoručně vygenerované důkazy činí zkreslení nepopiratelným.

### Klam utopených nákladů — hra „Investiční timeline"

**Trigger**: `component: "InvestmentTimeline"`

**UX flow:** Uživatel dostane briefing o projektu a kliknutím „investuje" 200 žetonů.
V sekvenci přicházejí tři aktualizace, každá ukazuje zhoršující se KPI.
Při každé aktualizaci: *„Pokračovat v investování (−100 žetonů) nebo zastavit ztráty?"*
Po sekvenci otázka Case zarámuje finální rozhodnutí. Výsledek odhalí „racionální bod výstupu"
oproti místu, kde zastavila většina uživatelů (a kde zastavil uživatel sám).

**Pedagogická hodnota**: Vysoká. Časový tlak a postupný závazek napodobují reálnou dynamiku sunk-cost.

### Ukotvení — další kandidát: slider „Mzdové vyjednávání"

**Trigger**: `component: "AnchorSlider"`

Před otázkou: jako výchozí pozice na mzdovém slideru se zobrazí „počáteční nabídka" zaměstnavatele.
Uživatel přetáhne slider na požadovanou částku. Výchozí pozice zkresluje finální volbu i v případě,
že ji uživatel aktivně upravuje. Bez roztáčení — čistší řešení pro méně dramatické, ale vysoce
praktické scénáře.

## Přehled tří case_type hodnot

| `case_type` | Popis | Backend? | Příklad komponenty |
|---|---|---|---|
| `"text"` | Stávající formát — statický scénář, výběr z možností | Ne | — |
| `"interactive"` | Vue komponenta předchází otázce; emituje `done` | Ne | `WheelOfFortune`, `FramingReveal` |
| `"multi_step"` | Iterativní hra s ohodnocením predikátu, sledování strategie | **Ano** | `RuleDiscovery` |

---

## Varianta multi_step — komponenta RuleDiscovery (confirmation bias)

### Motivace

Text-only formát Wasonova 2-4-6 úkolu je epistemologicky nedotažený: označuje strategii jako „racionální"
bez explicitního omezení třídy pravidel. Toto omezení nelze přirozeně vyjádřit v textu (viz Goodmanův
problém, Lagrangeova interpolace, neexistence uniformního prioru přes nekonečný prostor pravidel).

Multi-step formát problém obchází elegantně: **evaluuje empirické chování** (počet potvrzujících vs.
vyvracejících testů), nikoli formální optimalitu. Hodnotící kritérium je uzemněno v datech z Wasonova
experimentu (1960), ne v neprokázatelné epistemologické premise.

### UX flow

1. Aplikace náhodně vybere jedno pravidlo z knihovny (nebo přiřadí na základě obtížnosti uživatele).
2. Zobrazí se zárodková trojice (seed) a výzva: *„Hledám pravidlo. Navrhujte trojice — řeknu ANO nebo NE."*
3. Uživatel zadává trojice. Před každým testem volitelně vyjadřuje svou aktuální hypotézu (textové pole
   nebo výběr ze šablon). Toto umožňuje klasifikaci testu jako potvrzující / vyvracující.
4. Po každém testu backend synchronně vyhodnotí predikát a vrátí ANO/NE.
5. Uživatel může kdykoli prohlásit: *„Znám pravidlo."* a zapsat hypotézu. Aplikace pravidlo porovná.
6. Po vyčerpání max_tests nebo správném uhodnutí: reveal screen.

### Reveal screen

- Graf: poměr potvrzujících / vyvracejících testů uživatele vs. průměr Wasonova experimentu.
- Linie konvergence: kdy se hypotéza změnila.
- Srovnání: *„Strategii s vyvracejícími testy použili v experimentu ti, kteří pravidlo odhalili za 2,1 testu
  vs. 5,4 testu u těch, kteří potvrzovali."*

### Schéma rozšíření

```json
{
  "ui_hint": {
    "case_type": "multi_step",
    "component": "RuleDiscovery",
    "max_tests": 10,
    "randomize_rule": true,
    "track": ["confirming_tests", "disconfirming_tests", "hypothesis_changes", "tests_to_solution"],
    "reveal": {
      "wason_1960_confirming_only_avg_tests": 5.4,
      "wason_1960_disconfirming_avg_tests": 2.1
    },
    "rules": [
      {
        "id": "ascending",
        "seed": [2, 4, 6],
        "predicate": "a < b && b < c",
        "description_cs": "tři čísla ve vzestupném pořadí",
        "trap_hypothesis_cs": "čísla se zvyšují vždy o 2"
      },
      {
        "id": "arithmetic_progression",
        "seed": [3, 7, 11],
        "predicate": "b - a === c - b",
        "description_cs": "aritmetická posloupnost (stejné rozdíly)",
        "trap_hypothesis_cs": "vzestupná AP s rozdílem 4"
      },
      {
        "id": "geometric",
        "seed": [2, 6, 18],
        "predicate": "b * b === a * c",
        "description_cs": "geometrická posloupnost",
        "trap_hypothesis_cs": "násobí se vždy třemi"
      },
      {
        "id": "fibonacci_sum",
        "seed": [1, 2, 3],
        "predicate": "c === a + b",
        "description_cs": "třetí číslo = součet prvních dvou",
        "trap_hypothesis_cs": "po sobě jdoucí celá čísla"
      },
      {
        "id": "triangle_inequality",
        "seed": [3, 4, 5],
        "predicate": "a + b > c && b + c > a && a + c > b",
        "description_cs": "trojúhelníková nerovnost",
        "trap_hypothesis_cs": "Pythagorova trojice"
      }
    ]
  }
}
```

### Backend požadavky

Endpoint: `POST /api/v1/rule-test`

```json
{ "rule_id": "ascending", "triple": [5, 3, 8] }
→ { "result": false }
```

Predikáty se vyhodnocují server-side (zabránění podvádění inspekcí JS kódu). Pravidlo není v odpovědi
odhaleno — pouze výsledek ANO/NE. Obtížnost (`difficulty`: 1–5) umožňuje adaptivní přiřazení pravidla.

---

## Důsledky

**Pozitivní:**
- Cases se stávají skutečně zážitkovými; kognitivní past je navozena, ne jen popsána.
- JSON schéma Case zůstává zpětně kompatibilní (`ui_hint` je volitelné).
- `multi_step` řeší epistemologický problém text-only Wasonova formátu bez kompromisů.
- 8 pravidel s různou obtížností umožňuje znovuhratelnost a adaptivní obtížnost.

**Negativní / Rizika:**
- `interactive` komponenty: implementační úsilí ≈ 1–2 dny na komponentu, žádný backend.
- `multi_step` komponenty: vyžadují backend endpoint pro vyhodnocení predikátu + session stav.
- Přístupnost: animované komponenty musí podporovat `prefers-reduced-motion` a ovládání klávesnicí.
- A/B ukotvení u `WheelOfFortune` — analytika musí zaznamenat, která varianta kotvy byla podána.
- Klasifikace „potvrzující vs. vyvracující test" vyžaduje sledování uživatelovy aktuální hypotézy — UX výzva.

## Soubory

- `experiments/2026-05-prompt-evaluation/data/v1-plain/curated/interactive/opus-4.7__anchoring-textbook-01.json`
  — `interactive` tier; kompletní `ui_hint` pro `WheelOfFortune` (ukotvení).
- `experiments/2026-05-prompt-evaluation/data/v1-plain/curated/interactive/opus-4.7__confirmation_bias-textbook-02.json`
  — `interactive` tier; kompletní `ui_hint` pro `RuleDiscovery` s knihovnou 8 pravidel (konfirmační zkreslení).
