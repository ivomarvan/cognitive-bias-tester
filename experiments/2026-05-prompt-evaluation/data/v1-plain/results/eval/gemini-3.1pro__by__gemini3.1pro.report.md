# Report z hodnocení vygenerovaných příkladů

Tento report shrnuje hodnocení 40 testovacích příkladů na kognitivní zkreslení vygenerovaných modelem **Gemini 3.1 Pro**.

## Celkové výsledky

- **Celkové průměrné skóre:** 83.0 / 100
- **Učebnicové příklady (Textbook):** 83.5
- **Vlastní příklady (Own):** 82.7

### Průměry podle kritérií
- **Cognitive Trap:** 8.3 / 10
- **Rationality:** 8.9 / 10
- **Subtlety:** 7.0 / 10
- **Difficulty Adherence:** 7.9 / 10
- **Rule Adherence:** 9.0 / 10

## Shrnutí kvality

Generující model exceloval v kategoriích **Confirmation Bias** a **Sunk Cost Fallacy**, kde se mu podařilo vytvořit velmi uvěřitelné, reálné scénáře s jasnou logikou (např. *confirmation_bias-textbook-01* nebo *sunk_cost_fallacy-textbook-01*). 

**Největší slabina (Subtlety):** Mnoho nesprávných („biased“) odpovědí je formulováno příliš akademicky nebo jako sebereflexe. Místo toho, aby respondent přirozeně reagoval na situaci, analyzuje v textu odpovědi své vlastní zkreslení (např. *„Můj odhad bude ovlivněn tím...“*). To by v praxi prozradilo účel testu.

**Problémy se strukturou (Framing):** Dva příklady v kategorii Framing (framing-textbook-03, framing-own-04) musely být zamítnuty (auto-reject), protože porušily základní strukturální pravidlo. Buď nenabízely dvě ekvivalentní, odlišně nasvícené možnosti, nebo srovnávaly matematicky neporovnatelné hodnoty.

## Problematické příklady (Flagged)

Bylo nalezeno 3 problematických příkladů, které vyžadují zásadní úpravu nebo vyřazení:
- **framing-textbook-03** (Skóre: 69.0): reject. Důvody: cognitive_trap=4 (auto_reject)
- **framing-own-03** (Skóre: 57.0): reject. Důvody: cognitive_trap=4 (auto_reject), rationality=4 (auto_reject), weighted_score=57.0
- **framing-own-04** (Skóre: 69.0): needs_major_rewrite. Důvody: cognitive_trap=5

Doporučuje se zaměřit editorům primárně na kategorii Framing a u ostatních biasů projít všechny odpovědi a přepsat je do více hovorového, přirozenějšího jazyka bez explicitní sebereflexe respondenta.
