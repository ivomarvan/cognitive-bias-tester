# Zpráva o hodnocení generovaných příkladů (GPT-4)

Tato zpráva shrnuje hodnocení kvality vygenerovaných testovacích příkladů na kognitivní zkreslení (anchoring a framing) z modelu GPT-4.

## Celkové zhodnocení

Kvalita vygenerovaných příkladů je bohužel **velmi nízká**. Většina příkladů byla automaticky zamítnuta (`reject`) kvůli zásadním logickým nedostatkům nebo nedodržení formálních struktur pasti pro dané kognitivní zkreslení. Celkové průměrné vážené skóre se pohybuje hluboko pod hranicí použitelnosti (průměr 41.5 bodů ze 100).

### 1. Anchoring (Ukotvení)
U zkreslení typu anchoring model opakovaně chyboval ve formulaci „racionální“ odpovědi. Často předpokládal znalost externích informací, které nebyly v zadání zmíněny (např. nutnost rekonstrukce domu, konkrétní osobní rozpočet, atd.). Kvůli tomu racionální volby přestaly být objektivně doložitelné. V jednom případě model navíc logicky chyboval, když u aukce tvrdil, že cena půjde pod vyvolávací částku. Příklad `anchoring-own-04` byl jediný, který se přiblížil rozumné kvalitě a po úpravě by mohl být použit (`needs_major_rewrite`).

### 2. Framing (Rámování)
U framingu generátor vůbec nepochopil základní strukturní princip – aby mohl framing fungovat jako past, je nutné, aby dvě nabízené možnosti popisovaly **tutéž objektivní skutečnost**, přičemž jedna bude zarámovaná pozitivně a druhá negativně. Místo toho model generoval scénáře, kde volby reprezentovaly logicky ekvivalentní, ale nesrovnatelné postoje (např. interpretaci pozitiv a ignorování negativ), nebo testoval optimismus vs. pesimismus. To způsobilo automatické zamítnutí drtivé většiny těchto příkladů.

## Závěr a doporučení

Modely LLM zjevně selhávají v generování objektivně racionálních odpovědí a vyžadují mnohem explicitnější nápovědu (few-shot prompting) pro strukturální logiku zkreslení.

- **Pro tvůrce promptu:** Bude nutné poskytnout generátoru detailní „gold standard“ příklady toho, jak přesně má vypadat volba pro *framing* a jak zajistit, aby *racionální* odpověď u *anchoringu* nevycházela z nepodložených předpokladů.
- **Pro editora:** Aktuální výstup nelze pro vzdělávací aplikaci použít. Skoro všechny příklady vyžadují buď podstatný přepis (`needs_major_rewrite`), nebo jejich kompletní vyřazení (`reject`).