# Úkol: Vytvoření zlatých jednoduchých (few-shot) příkladů pro případy kognitivních zkreslení

## Vaše role

Jste expert na kognitivní psychologii, behaviorální ekonomii a návrh vzdělávacího obsahu.
Vytváříte **případy ve zlatém standardu**, které budou vloženy do promptů pro AI jako
few-shot ukázky. Jejich kvalita přímo určuje kvalitu všech následně generovaných případů
v produkčním systému.

Nejde o kreativní cvičení — jde o precizní práci. Každý případ bude nezávisle kontrolován.
Snažte se o to nejlepší, co dokážete.

---

## Jazyk výstupu

**Čeština.** Všechna pole `title`, `question`, `options.text` a `explanation` musí být
v přirozené, současné češtině. Klíče JSON zůstávají anglicky.

---

## Formát výstupu

Vygenerujte **přesně 5 JSON objektů** — jeden pro každý typ zkreslení níže.
Výstup ve formě JSON pole. Žádné markdownové bloky kódu, žádný komentář mimo pole.

Povinné schéma pro každý případ:
```json
{
  "bias_type_slug": "string — jeden z 5 slugů níže",
  "title": "string — krátký název scénáře, max 10 českých slov",
  "question": "string — realistický scénář (3–5 vět) + otázka pro uživatele",
  "options": [
    {"label": "A", "text": "string — možnost odpovědi v češtině"},
    {"label": "B", "text": "string — možnost odpovědi v češtině"},
    {"label": "C", "text": "string — možnost odpovědi v češtině"},
    {"label": "D", "text": "string — možnost odpovědi v češtině"}
  ],
  "correct_option": 0,
  "explanation": "string — 3–4 věty v češtině: jaké zkreslení nastalo, proč správná možnost mu předchází, jaký je racionální postup",
  "parametric_payload": {}
}
```

---

## Pět typů zkreslení

### 1. `anchoring` — Ukotvení

**Definice:** První prezentovaná číselná informace („kotva“) má neúměrný vliv na všechny
následné odhady a rozhodnutí, i když je kotva svévolná či irelevantní.

**Strukturální požadavek:** Scénář MUSÍ explicitně uvést číslo, cenu nebo množství jako první
referenční bod. Iracionální chování spočívá v tom, že se člověk nechá táhnout k této kotvě
místo nezávislého uvažování nebo dat.

**Typické vzory:** vyjednávání platu vycházející z libovolné částky; „původní cena“ výrobku,
kvůli níž se zdá akční cena výhodná; počáteční lékařský odhad zkreslující očekávání pacienta.

---

### 2. `framing` — Rámování

**Definice:** Stejná objektivní skutečnost nebo volba vede k různým rozhodnutím podle toho,
jak je prezentována — jako zisk, ztráta, procento nebo absolutní číslo.

**Strukturální požadavek:** Scénář MUSÍ nabídnout DVĚ nebo více možností, které jsou logicky
ekvivalentní, ale jsou formulovány jinak. Iracionální chování je volba podle rámu, ne podle
skutečnosti pod tím.

**Typické vzory:** „90% přežití“ vs. „10% úmrtnost“; „zachrání 200 životů“ vs. „400 zemře“;
„obsahuje 10 % tuku“ vs. „90 % bez tuku“; politik líčí nezaměstnanost jako „3 % bez práce“
vs. „97 % zaměstnáno“.

---

### 3. `loss_aversion` — Averze ke ztrátě

**Definice:** Ztráty psychologicky přibližně dvakrát silněji rezonují než srovnatelné zisky.
Kvůli tomu lidé podstupují iracionální rizika, aby se ztrátě vyhnuli, nebo iracionálně
odmítají rizika, která by mohla přinést zisk.

**Strukturální požadavek:** Scénář MUSÍ volbu explicitně rámovat jako potenciální ztrátu na
jedné straně a potenciální zisk na druhé, přičemž očekávané hodnoty jsou vyrovnané nebo je
racionální volbou varianta „zisku“, ale postava iracionálně zvolí cestu „vyhýbání se ztrátě“.

**Typické vzory:** odmítnutí sázky 50/50, protože možná ztráta bolí víc než srovnatelný možný
zisk; držení klesající akcie, protože prodej „připadá“ jako přiznání ztráty; placení za prodlouženou
záruku u levného spotřebiče.

---

### 4. `confirmation_bias` — Konfirmační zkreslení

**Definice:** Sklon vyhledávat, interpretovat, upřednostňovat a vybavovat si informace,
které potvrzují již existující přesvědčení, zatímco protichůdné důkazy ignorujeme.

**Strukturální požadavek:** Scénář MUSÍ ukázat postavu, která už něčemu věří, a poté čelí novým
informacím. Iracionální chování je selektivní přijímání potvrzujících důkazů a zpochybňování
(nebo nevyhledávání) vyvracejících důkazů.

**Typické vzory:** manažer, který se už rozhodl pro kandidáta, čte životopis jen „pro silné
stránky“; investor věřící v akcii ignoruje negativní analytické zprávy; člověk si přes vyhledávač
„sám diagnozuje“ vážnou nemoc a kliká jen na výsledky, které mu dávají za pravdu.

---

### 5. `sunk_cost_fallacy` — Klam utopených nákladů

**Definice:** Pokračování v neúspěšné linii jednání kvůli dříve investovaným zdrojům (peníze,
čas, úsilí), které už nelze získat zpět, místo aby se hodnotily jen budoucí náklady a přínosy.

**Strukturální požadavek:** Scénář MUSÍ být jasné, že náklad už byl vynaložen a je nevratný.
Iracionální chování je nechat tuto minulou investici řídit budoucí rozhodnutí místo toho, aby se
zhodnotilo, co dává smysl dál.

**Typické vzory:** dočtení špatné knihy, protože za ni člověk zaplatil; pokračování v neúspěšném
projektu, protože tým na něm strávil dva roky; setrvání v kariéře, která nevyhovuje, protože
člověk platil za titul; snězení špatného jídla v restauraci, protože bylo drahé.

---

## Kvalitativní kritéria (každý případ se jimi bude ověřovat)

| Kritérium | Požadavek |
|-----------|-----------|
| **Čistota zkreslení** | Scénář přesně demonstruje dané zkreslení — jiné zkreslení není věrohodnější vysvětlení |
| **Realistický scénář** | Mohlo by se stát současnému dospělému Čechu; ne abstrakce z učebnice |
| **Věrohodnost možností** | Všechny 4 možnosti musí být uvěřitelné odpovědi; žádná nesmí být zjevně hloupá |
| **Jasnost správné možnosti** | Správná možnost je racionální a obhajitelná, ale ne triviálně zřejmá |
| **Rozložení `correct_option`** | Nepoužívejte u všech 5 případů jen index 0 nebo 1 — rozložte mezi 0, 1, 2, 3 |
| **Hloubka vysvětlení** | Jmenuje zkreslení, vysvětlí mechanismus, popíše racionální alternativu |
| **Čeština** | Přirozená, současná čeština; ne přehnaně knižní ani „přeložený“ dojem |
| **Náročnost** | Mělo by přimět k zamyšlení — ne hádanka pro psychologa |

---

## Antivzory, kterým se vyhněte

- ❌ Příliš abstraktní scénáře („Představte si, že jste investovali $X…“)
- ❌ Možnosti, z nichž je jedna zjevně vtip nebo společensky nepřijatelné chování
- ❌ Vysvětlení, které říká jen „kvůli zkreslení“, aniž by popsal mechanismus
- ❌ Scénáře, kde stejně dobře sedí více zkreslení najednou
- ❌ Použití slov „zkreslení“ / „bias“ přímo v textu scénáře
- ❌ Identická struktura scénářů napříč různými typy zkreslení

---

## Výstup

Vygenerujte 5 případů jako jedno JSON pole. Začněte `[` a končte `]`.
Žádný jiný text před tím ani po tom.
