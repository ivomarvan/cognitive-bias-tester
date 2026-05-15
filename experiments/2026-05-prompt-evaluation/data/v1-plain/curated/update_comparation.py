#!/usr/bin/env python3
"""Add eval_comparation field to all curated JSON files based on Sonnet 4.6 review."""

import json
from pathlib import Path

BASE = Path(__file__).parent

# Mapping: relative path → (preferred, reason)
# "n/a" = no Gemini suggestion was provided
COMPARATIONS: dict[str, tuple[str, str]] = {
    # ── good/anchoring ────────────────────────────────────────────────────────
    "good/anchoring/opus-4.7__anchoring-own-01.json": (
        "gemini",
        "Vivid scene ('procházení elektrem', 'to je pecka') vs. strojené 'Je třeba "
        "rozhodnout o nákupu'. Gemini výrazně přirozenější bez ztráty přesnosti.",
    ),
    "good/anchoring/opus-4.7__anchoring-own-03.json": (
        "gemini",
        "Cestovní kontext a prohlížení webu ('letní dovolená', 'Hned vedle na webu') "
        "věrnější realitě. Biased volba přesvědčivější ('sleva přes dvanáct tisíc se "
        "přece neodmítá' vs. 'sleva 12 200 Kč je výrazná').",
    ),
    "good/anchoring/opus-4.7__anchoring-own-05.json": (
        "original",
        "Gemini vypustil klíčový údaj o poklesu zisku o 22 %, který racionální volbu "
        "(nekoupit) opravňuje. Ztráta přesnosti snižuje edukační hodnotu příkladu "
        "difficulty-5.",
    ),
    "good/anchoring/opus-4.7__anchoring-textbook-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/anchoring/opus-4.7__anchoring-textbook-02.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/anchoring/opus-4.7__anchoring-textbook-03.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    # ── good/confirmation_bias ────────────────────────────────────────────────
    "good/confirmation_bias/opus-4.7__confirmation_bias-own-05.json": (
        "gemini",
        "Přirozený vývojářský dialog ('béčko', 'schválně najdu taková data'). Vyhýbá "
        "se neohrabanému genderově neutrálnímu 'vývojář/ka' originálu.",
    ),
    "good/confirmation_bias/opus-4.7__confirmation_bias-textbook-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/confirmation_bias/opus-4.7__confirmation_bias-textbook-02.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    # ── good/framing ─────────────────────────────────────────────────────────
    "good/framing/opus-4.7__framing-own-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/framing/opus-4.7__framing-own-02.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/framing/opus-4.7__framing-own-03.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/framing/opus-4.7__framing-own-04.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/framing/opus-4.7__framing-own-05.json": (
        "original",
        "Geminiho 'méně než 5 %' je ekvivalent okamžitě viditelný; originální "
        "'1 procentní bod nižší než 6 %' vyžaduje výpočet 100-(6-1)=95 %, který je "
        "záměrným pedagogickým jádem difficulty-5. Gemini příklad zásadně oslabuje.",
    ),
    "good/framing/opus-4.7__framing-textbook-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/framing/opus-4.7__framing-textbook-02.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/framing/opus-4.7__framing-textbook-03.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    # ── good/loss_aversion ───────────────────────────────────────────────────
    "good/loss_aversion/opus-4.7__loss_aversion-own-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-own-02.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-own-03.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-own-04.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-own-05.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-textbook-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-textbook-02.json": (
        "gemini",
        "Autentičtější vnitřní hlas ('přece se nevzdám své vlastní věci jen tak lacino'). "
        "Explanace explicitně pojmenovává efekt vlastnictví. Slabina: Gemini předpokládá "
        "mužský rod ('Řekl bych si').",
    ),
    "good/loss_aversion/opus-4.7__loss_aversion-textbook-03.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    # ── good/sunk_cost_fallacy ───────────────────────────────────────────────
    "good/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-own-01.json": (
        "gemini",
        "Konkrétní pokušení ('čerstvé, lákavé vafle' vs. generické 'další chody'). "
        "Tělesná konkrétnost ('pocit nacpání a těžkého břicha') je silnější past pro "
        "difficulty-1.",
    ),
    "good/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-own-04.json": (
        "gemini",
        "Výjimečně autentická past ('pět let dřiny', 'z korporátu'). Racionální hlas "
        "je rozhodný ('Práci beru. Dělat další dva roky na titulu, který nevyužiju, mi "
        "absolutně nedává smysl').",
    ),
    "good/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-own-05.json": (
        "gemini",
        "Silná emocionální intenzita sunk-cost myšlení ('spláchnout do záchodu'). "
        "Racionální odpověď přirozeně prezentuje výpočet budoucích toků a zachovává "
        "všechna numerická data.",
    ),
    "good/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-textbook-01.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-textbook-02.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    "good/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-textbook-03.json": (
        "n/a",
        "Gemini nenavrhl alternativu — příklad hodnotil jako dostatečně kvalitní.",
    ),
    # ── borderline/anchoring ─────────────────────────────────────────────────
    "borderline/anchoring/opus-4.7__anchoring-own-02.json": (
        "gemini",
        "Zachovává všechna klíčová data a přidává přirozený hovorový tón pohovoru. "
        "První osoba ('Řeknu si', 'Nechám personalistu') věrnější skutečnému "
        "rozhodovacímu procesu.",
    ),
    "borderline/anchoring/opus-4.7__anchoring-own-04.json": (
        "gemini",
        "Živý reklamní kontext ('Na internetu na vás vyskočí reklama'). Biased volba "
        "přirozeněji odhaluje myšlení ('reálně bych za ty konzultace dal jinak skoro "
        "šedesát tisíc'). Slabina: racionální volba nezmiňuje doporučený počet 4-6 "
        "sezení z originálu.",
    ),
    # ── borderline/confirmation_bias ─────────────────────────────────────────
    "borderline/confirmation_bias/opus-4.7__confirmation_bias-own-01.json": (
        "gemini",
        "Přirozená scéna prohlížení recenzí. 'Schválně si vyfiltruji' živější než "
        "'Cíleně projít'. Vyhýbá se neohrabanému 'Vybral/a jste si' originálu.",
    ),
    "borderline/confirmation_bias/opus-4.7__confirmation_bias-own-02.json": (
        "gemini",
        "Lepší zasazení do scény. Biased volba ('web výrobce, jestli tam ostatní lidé "
        "popisují stejné zlepšení') věrněji zachycuje confirmation seeking než "
        "originálovo formální 'Přečíst svědectví'.",
    ),
    "borderline/confirmation_bias/opus-4.7__confirmation_bias-own-03.json": (
        "gemini",
        "Přirozené prostředí pohovoru místo formálního 'Jako náborář/ka vedete "
        "strukturovaný pohovor'. Vyhýbá se 'náborář/ka'. Poznámka: 'Zkusím na něj "
        "zatlačit' předpokládá mužský rod kandidáta.",
    ),
    "borderline/confirmation_bias/opus-4.7__confirmation_bias-own-04.json": (
        "gemini",
        "Zasazení do zprávy ('Všimli jste si nedávné zprávy') je pro běžného uživatele "
        "přirozenější než perspektiva výzkumníka. Metodologický obsah zachován.",
    ),
    "borderline/confirmation_bias/opus-4.7__confirmation_bias-textbook-03.json": (
        "gemini",
        "Večírkové prostředí ('Na večírku se dáte do řeči') výrazně přirozenější než "
        "formální 'Máte za úkol'. Sociální kontext dělá confirmation bias živějším.",
    ),
    # ── borderline/sunk_cost_fallacy ─────────────────────────────────────────
    "borderline/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-own-02.json": (
        "gemini",
        "Přirozená scéna ('roční permanentka na druhém konci města'). Neutrální volba "
        "realistická ('aspoň pod cenou prodat nebo přepsat na nějakého kamaráda').",
    ),
    "borderline/sunk_cost_fallacy/opus-4.7__sunk_cost_fallacy-own-03.json": (
        "gemini",
        "Hovorové 'Vykašlu se na ně' zachycuje emocionální uvolnění při přijetí "
        "utopených nákladů. 'Ten zaplacený kurz dojedu až do konce, přece ty vyhozené "
        "peníze nenechám jen tak...' autentičtější biased hlas.",
    ),
}


def update_file(rel_path: str, preferred: str, reason: str) -> None:
    path = BASE / rel_path
    if not path.exists():
        print(f"  SKIP (not found): {rel_path}")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("evaluation", {}).setdefault("sonnet4.6", {})
    data["evaluation"]["sonnet4.6"]["eval_comparation"] = {
        "prefered": preferred,
        "reason": reason,
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK [{preferred:8}]: {rel_path}")


def main() -> None:
    print(f"Updating {len(COMPARATIONS)} files in {BASE}\n")
    for rel_path, (preferred, reason) in COMPARATIONS.items():
        update_file(rel_path, preferred, reason)
    print("\nDone.")


if __name__ == "__main__":
    main()
