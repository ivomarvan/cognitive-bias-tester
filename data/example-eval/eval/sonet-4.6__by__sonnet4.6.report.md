# Hodnocení sady příkladů: Claude Sonnet 4.6 (sebeevaluace)

**Hodnotitel:** Claude Sonnet 4.6  
**Datum:** 2026-05-10  
**Celkové průměrné skóre:** 77,9 / 100  
**Flagovaných příkladů:** 0 z 40  

> **Poznámka:** Toto hodnocení je sebeevaluací — hodnotitel je totožný s generátorem. Tato skutečnost může způsobit hodnotitelský bias a výsledky je nutné interpretovat s rezervou.

---

## Celkové hodnocení

Claude Sonnet 4.6 produkuje strukturálně konzistentní sadu bez flagovaných příkladů. Silnými stránkami jsou přesná numerická data v anchoring, explicitní EV výpočty v loss_aversion a korektní difficulty kalibrace napříč celou sadou. Slabinami jsou drobné tematické překryvy ve framing (dvě potravinářské příklady) a confirmation_bias (dva nákupní scénáře).

---

## Výsledky podle bias kategorie

| Bias | N | Průměr | Min | Max | use_as_is | needs_edit | needs_rewrite | reject |
|---|---|---|---|---|---|---|---|---|
| anchoring | 8 | 77,2 | 72,5 | 83,5 | 0 | 8 | 0 | 0 |
| framing | 8 | 77,5 | 75,0 | 82,0 | 0 | 8 | 0 | 0 |
| loss_aversion | 8 | 79,1 | 73,5 | 88,5 | 1 | 7 | 0 | 0 |
| confirmation_bias | 8 | 77,2 | 73,5 | 82,0 | 0 | 8 | 0 | 0 |
| sunk_cost_fallacy | 8 | 78,4 | 73,5 | 82,0 | 0 | 8 | 0 | 0 |

---

## Top příklady

1. **loss_aversion-own-05** (88,5) — pojistka 120 eur, EV=80 eur: všechna čísla pro výpočet explicitně dostupná.
2. **anchoring-own-04** (83,5) — charity preset buttons: jemná, realistická past.
3. **framing-own-05** (82,0) — klinická studie NTT=100: výborný difficulty-5 příklad s explicitními metrikami.

---

## Silné stránky

- **Žádné prohozené verdikty** — všechny biased/rational/neutral verdikty jsou konzistentní s textem.
- **Explicitní data ve všech sekcích** — anchoring obsahuje vždy cotvu a srovnávací data; loss_aversion explicitní EV.
- **Přesná difficulty kalibrace** — vlastní příklady pokrývají rozsah 1–5 přesně.
- **Zakázané domény vynechány** — žádná politická, náboženská nebo jinak problematická témata.
- **Kulturní neutralita** — použité scénáře jsou mezinárodně srozumitelné (euro, ne Kč u většiny).

---

## Slabiny

### 1. Tematické překryvy ve framing
- framing-textbook-02 (mleté maso) a framing-own-01 (jogurt) obě využívají potravinářský framing X% bez tuku. Obsah a typ produktu jsou dostatečně odlišné, ale struktura je velmi podobná. Doporučit výměnu jednoho za scénář z jiné domény.

### 2. Tematické překryvy v confirmation_bias
- confirmation_bias-own-01 (fotoaparát + recenze) a confirmation_bias-own-02 (akcie + zpravodajství) jsou oba "nákupní rozhodnutí + hledání informací". Struktura je dostatečně odlišná, ale variace domén by byla vítána.

### 3. Délka otázek u difficulty-5 příkladů
- loss_aversion-own-05 a framing-own-05 mírně překračují doporučený limit ~60 slov. Akceptovatelné pro difficulty 5, ale kurátorovi doporučujeme zkonzultovat.

---

## Srovnání s ostatními modely

| Model | Průměr | Flagovaných | REJECT |
|---|---|---|---|
| **GPT-5.5** | 80,3 | 0/40 | 0 |
| **Claude Sonnet 4.6** | 77,9 | 0/40 | 0 |
| **Gemini 3.1 Pro** | 75,0 | 3/40 | 2 |
| GPT-4o | 43,8* | 14/16* | 13* |
| GPT-4o-mini | 39,1 | 37/40 | 30 |

\* pouze 16 příkladů z 40 (neúplný soubor)

GPT-5.5 je celkově nejsilnější (80,3 vs. 77,9), zejména díky vyšší kvalitě anchoring sekce. Claude Sonnet 4.6 má výhodu v konzistentní difficulty kalibraci a absence překryvů v sunk_cost.

---

## Doporučení pro kurátora

Pro produkci gold examples doporučujeme kombinovat nejlepší příklady z **GPT-5.5** a **Claude Sonnet 4.6**:
- Z GPT-5.5: anchoring sekci, sunk_cost sekci
- Ze Sonnet 4.6: loss_aversion sekci (explicitní EV výpočty), framing-own-03 (auto, poplatek vs. sleva)

Gemini 3.1 Pro je třetí nejlepší sada a může poskytnout doplňkové příklady pro sunk_cost_fallacy a confirmation_bias po drobných úpravách.
