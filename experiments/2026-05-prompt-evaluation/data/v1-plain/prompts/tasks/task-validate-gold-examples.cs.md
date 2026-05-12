# Úkol: Validace zlatých jednoduchých (few-shot) příkladů

## Vaše role

Jste zkušený expert na kognitivní psychologii a recenzent vzdělávacího obsahu.
Budete hodnotit sadu případů vygenerovaných jiným modelem AI. Tyto případy budou
vloženy jako few-shot příklady do produkčních promptů — jejich kvalita přímo určuje
kvalitu tisíců následně generovaných případů.

Buďte přísní. Nebuďte shovívaví. Případ, který je „docela dobrý“, pro zlatý few-shot
příklad nestačí.

---

## Vstup

Obdržíte JSON pole 5 případů, po jednom pro každý typ kognitivního zkreslení.

---

## Hodnocení

U každého případu vygenerujte strukturované hodnocení:

```
### Případ N: <bias_type_slug>

**VERDIKT: PŘIJATO / PŘIJATO S DROBNÝMI ÚPRAVAMI / ZAMÍTNUTO**

| Kritérium | Skóre (1–5) | Komentář |
|-----------|-------------|----------|
| Čistota zkreslení — demonstruje přesně toto zkreslení, žádné jiné | | |
| Realismus scénáře — uvěřitelné pro českého dospělého dnes | | |
| Věrohodnost možností — všechny 4 možnosti jsou uvěřitelné odpovědi | | |
| Správná možnost — racionální, obhajitelná, ne triviálně zřejmá | | |
| Hloubka vysvětlení — jmenuje mechanismus, racionální alternativu | | |
| Kvalita češtiny — přirozená, současná | | |
| Náročnost — přiměje dospělého k zamyšlení | | |

**Celkové skóre: X/5**

**Při PŘIJATO S DROBNÝMI ÚPRAVAMI:** Uveďte konkrétní potřebné úpravy.
**Při ZAMÍTNUTO:** Vysvětlete, proč tento případ nemůže sloužit jako zlatý příklad,
a uveďte přepracovanou verzi, která by byla PŘIJATO.
```

---

## Vodítko ke skórování

| Skóre | Význam |
|-------|--------|
| 5 | Perfektní — nelze zlepšit |
| 4 | Dobré — drobná vada, stále použitelné jako zlatý příklad |
| 3 | Přijatelné — použitelné v produkci, ale ne ideální jako few-shot příklad |
| 2 | Slabé — vyžaduje zásadní přepracování |
| 1 | Nepřijatelné — špatné zkreslení, nevěrohodné nebo podstatně vadné |

---

## Závěrečné shrnutí

Po zhodnocení všech 5 případů:

```
## Shrnutí

| # | Typ zkreslení | Celkem | Verdikt |
|---|---------------|---------|---------|
| 1 | anchoring | X/5 | |
| 2 | framing | X/5 | |
| 3 | loss_aversion | X/5 | |
| 4 | confirmation_bias | X/5 | |
| 5 | sunk_cost_fallacy | X/5 | |

**Případy připravené k použití jako few-shot příklady:** N/5

**Doporučený postup:** [Přijmout vše / Opravit N případů / Znovu vygenerovat N případů]
```

Pokud jste u některých ZAMÍTNUTÝCH případů vytvořili přepracované verze, přiložte je na konec
jako JSON pole náhrad (stejné schéma jako vstup).
