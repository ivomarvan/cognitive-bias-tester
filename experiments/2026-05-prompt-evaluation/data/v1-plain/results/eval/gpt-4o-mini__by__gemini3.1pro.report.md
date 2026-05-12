# Hodnotící zpráva: GPT-4o-mini

**Hodnotitel:** Gemini 3.1 Pro
**Datum:** 2026-05-10T20:11:17+02:00
**Celkové průměrné skóre:** 41.7/100

## Manažerské shrnutí
Generující model GPT-4o-mini hrubě selhal ve většině kategorií. Největším problémem je naprostá absence 'objektivní racionality' v odpovědích — generátor si často plete racionální volbu s opačným extrémem, subjektivním názorem nebo generuje matematicky totožné odpovědi (typické pro framing). Mnohé příklady (hlavně na loss aversion a anchoring) tak nejsou validní testy kognitivních zkreslení, ale otázky na osobní preference bez správné odpovědi. Použitelný je jen malý zlomek vygenerovaného obsahu.

## Hlavní problémy
- **Selhání v objektivní racionalitě:** U anchoringu a framingu model často vygeneroval možnosti, které znamenaly naprosto to samé (např. 5 % vs každý dvacátý), a jednu nesmyslně označil za racionální.
- **Záměna biasů:** Některé příklady prezentované jako ztrátová averze (loss aversion) nebo kotvení (anchoring) byly ve skutečnosti zcela jiné biasy, případně nedávaly žádný psychologický smysl.
- **Subjektivita:** Místo logických hádanek model generoval dotazníkové otázky na náladu či preference, které postrádají 'správnou' racionální odpověď.

## Statistiky podle typu zkreslení
- **anchoring**: průměr 21.6 (min 5.0, max 31.0)
- **framing**: průměr 29.3 (min 13.0, max 46.0)
- **loss_aversion**: průměr 28.3 (min 18.5, max 43.0)
- **confirmation_bias**: průměr 68.4 (min 57.5, max 74.0)
- **sunk_cost_fallacy**: průměr 60.9 (min 31.0, max 80.0)

## Nejlepší příklady (Top 3)
- sunk_cost_fallacy-textbook-02
- sunk_cost_fallacy-own-01
- sunk_cost_fallacy-own-03

## Nejhorší příklady (Bottom 3)
- anchoring-textbook-02
- framing-textbook-03
- loss_aversion-textbook-02

## Doporučení pro kurátora
Z celkových 40 příkladů jich bylo **28 označeno flagem (flagged)**, což znamená, že valná většina datasetu byla automaticky zamítnuta (auto-reject kvůli skóre racionality nebo pasti menšímu než 5).
Model pro tento úkol nebyl dostatečně instruován, nebo nemá dostatečnou kapacitu pochopit strukturální požadavky kognitivních testů. Doporučuji použít mnohem silnější model (např. GPT-4o, Claude 3.5 Sonnet) pro další generování.