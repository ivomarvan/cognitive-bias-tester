import json
import hashlib
from datetime import datetime

# Vstup a výstup
INPUT_FILE = "/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/gen/gpt-4o-mini.json"
OUTPUT_JSON = "/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/eval/gpt-4o-mini__by__gemini3.1pro.json"
OUTPUT_MD = "/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/eval/gpt-4o-mini__by__gemini3.1pro.report.md"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    input_data = json.load(f)

# Hardcoded evaluations
evals = {
    "anchoring-textbook-01": {"t": 2, "r": 0, "s": 5, "d": 2, "ru": 7, "fb": "Není to funkční past, 500 Kč je prostě cena trička. Racionální odpověď postrádá logický základ.", "str": [], "weak": ["Chybí objektivní racionalita", "Neodpovídá principu anchoringu"], "fix": "Nahradit scénář odhadem neznámé hodnoty na základě nesouvisející kotvy."},
    "anchoring-textbook-02": {"t": 0, "r": 0, "s": 0, "d": 0, "ru": 5, "fb": "Zcela špatný příklad, odpovědi 20 % a 20 ze 100 jsou matematicky totožné.", "str": [], "weak": ["Odpovědi jsou identické", "Nejde o anchoring, spíše pokus o framing", "Nulová racionalita"], "fix": "Zcela přepsat."},
    "anchoring-textbook-03": {"t": 2, "r": 0, "s": 4, "d": 2, "ru": 7, "fb": "Předchozí výsledek není nezávislá kotva, ale relevantní informace o formě týmu. Odpověď nelze objektivně spočítat.", "str": [], "weak": ["Záměna anchoringu za predikci trendu", "Chybí logická opora pro racionální odpověď"], "fix": "Zcela přepsat."},
    "anchoring-own-01": {"t": 3, "r": 2, "s": 4, "d": 2, "ru": 7, "fb": "Otázka se ptá na subjektivní požadavek, neexistuje jedna objektivně správná mzda.", "str": [], "weak": ["Otázka nemá jednoznačně racionální řešení", "Slabá past"], "fix": "Zcela přepsat."},
    "anchoring-own-02": {"t": 0, "r": 2, "s": 3, "d": 2, "ru": 7, "fb": "Tlak na další prohlídce silně koreluje s minulým, nejedná se o kognitivní zkreslení, ale logický předpoklad.", "str": [], "weak": ["Nejde o anchoring, ale predikci z minulých dat", "Racionální odpověď je diskutabilní"], "fix": "Zcela přepsat."},
    "anchoring-own-03": {"t": 2, "r": 0, "s": 4, "d": 2, "ru": 7, "fb": "Cena nového koncertu závisí na interpretovi, průměr z minulých koncertů není relevantní kotva.", "str": [], "weak": ["Chybí objektivní řešení", "Nejedná se o čistý anchoring"], "fix": "Zcela přepsat."},
    "anchoring-own-04": {"t": 2, "r": 0, "s": 3, "d": 2, "ru": 7, "fb": "Subjektivní rozhodnutí o dárku nemá jedinou správnou racionální odpověď.", "str": [], "weak": ["Subjektivní preference místo racionality", "Neodpovídá definici zkreslení"], "fix": "Zcela přepsat."},
    "anchoring-own-05": {"t": 2, "r": 2, "s": 4, "d": 2, "ru": 7, "fb": "Obchodní strategie nemá jednoznačně správné řešení, obě volby mohou být racionální v různém kontextu.", "str": [], "weak": ["Chybí objektivní racionalita", "Konkurence není kognitivní kotva, ale tržní faktor"], "fix": "Zcela přepsat."},

    "framing-textbook-01": {"t": 5, "r": 0, "s": 2, "d": 2, "ru": 7, "fb": "Obě metody jsou statisticky identické (90 % úspěšnost = 10 % neúspěšnost), žádná není objektivně 'racionálnější'.", "str": [], "weak": ["Odpovědi popisují stejnou volbu", "Žádná volba není objektivně lepší"], "fix": "Zcela přepsat."},
    "framing-textbook-02": {"t": 5, "r": 0, "s": 2, "d": 2, "ru": 7, "fb": "Stejná chyba jako výše, obě investice mají stejnou pravděpodobnost, žádná není 'racionální'.", "str": [], "weak": ["Odpovědi jsou identické", "Chybí racionalita"], "fix": "Zcela přepsat."},
    "framing-textbook-03": {"t": 0, "r": 0, "s": 2, "d": 2, "ru": 7, "fb": "Toto není framing s volbou, ale otázka na názor. Obě odpovědi jsou označeny jako biased.", "str": [], "weak": ["Neobsahuje racionální volbu", "Špatná struktura testu"], "fix": "Zcela přepsat."},
    "framing-own-01": {"t": 4, "r": 2, "s": 3, "d": 2, "ru": 7, "fb": "Otázka se ptá na reakci, ne na rozhodnutí. Hodnocení je ryze subjektivní.", "str": [], "weak": ["Nejde o rozhodovací problém", "Racionalita je zcela subjektivní"], "fix": "Zcela přepsat."},
    "framing-own-02": {"t": 3, "r": 0, "s": 2, "d": 2, "ru": 7, "fb": "5 % a 'každý dvacátý' znamenají přesně to samé. Nelze jednu označit za racionální.", "str": [], "weak": ["Identické odpovědi", "Chybí racionální složka"], "fix": "Zcela přepsat."},
    "framing-own-03": {"t": 4, "r": 2, "s": 3, "d": 2, "ru": 7, "fb": "Opět otázka na reakci, ne rozhodnutí mezi ekvivalentními možnostmi.", "str": [], "weak": ["Neexistuje objektivně správná reakce", "Nesplňuje formát framingu"], "fix": "Zcela přepsat."},
    "framing-own-04": {"t": 4, "r": 2, "s": 3, "d": 2, "ru": 7, "fb": "Ptá se na pocit, nikoliv na objektivní fakt nebo volbu.", "str": [], "weak": ["Subjektivní pocit nelze hodnotit jako racionální", "Chybný formát"], "fix": "Zcela přepsat."},
    "framing-own-05": {"t": 6, "r": 3, "s": 5, "d": 3, "ru": 7, "fb": "Nejde o framing, ale o skryté poplatky. 6 % - 1 % nemusí být lepší než 5 % podle základu výpočtu.", "str": [], "weak": ["Jde spíše o matematický chyták než framing", "Racionalita předpokládá nejasné skutečnosti"], "fix": "Zcela přepsat."},

    "loss_aversion-textbook-01": {"t": 4, "r": 0, "s": 5, "d": 2, "ru": 7, "fb": "Nelze určit očekávanou hodnotu projektu (neznáme částku výhry), takže nelze stanovit racionální volbu.", "str": [], "weak": ["Chybí matematický základ pro racionalitu", "Neúplné zadání"], "fix": "Doplnit konkrétní částky pro výpočet očekávané hodnoty."},
    "loss_aversion-textbook-02": {"t": 2, "r": 0, "s": 3, "d": 2, "ru": 5, "fb": "Odpověď 'Odevzdat vakcínu' nedává smysl. Scénář je zmatený a nelogický.", "str": [], "weak": ["Nesmyslný scénář", "Nelogické možnosti"], "fix": "Zcela přepsat."},
    "loss_aversion-textbook-03": {"t": 3, "r": 0, "s": 4, "d": 2, "ru": 7, "fb": "Zda nasadit zraněného hráče nelze objektivně označit za racionální (riziko trvalých následků).", "str": [], "weak": ["Racionalita je silně subjektivní", "Závisí na neznámých proměnných"], "fix": "Zcela přepsat."},
    "loss_aversion-own-01": {"t": 5, "r": 0, "s": 5, "d": 2, "ru": 7, "fb": "Zda akcie prodat nebo držet po poklesu nelze označit za objektivně racionální bez znalosti budoucího vývoje.", "str": [], "weak": ["Absence objektivně racionální volby", "Ignoruje fundamentální analýzu"], "fix": "Zcela přepsat."},
    "loss_aversion-own-02": {"t": 4, "r": 4, "s": 5, "d": 3, "ru": 7, "fb": "Volba zaplatit za prevenci je logická, ale formulace 'riskovat komplikace' silně napovídá.", "str": [], "weak": ["Zjevná nápověda v textu", "Slabá past"], "fix": "Zcela přepsat."},
    "loss_aversion-own-03": {"t": 2, "r": 0, "s": 4, "d": 2, "ru": 7, "fb": "Platba za kroužky z obavy o neúspěch není loss aversion v klasickém pojetí. Subjektivní volba.", "str": [], "weak": ["Neodpovídá typu zkreslení", "Chybí racionalita"], "fix": "Zcela přepsat."},
    "loss_aversion-own-04": {"t": 4, "r": 0, "s": 5, "d": 2, "ru": 7, "fb": "Racionalita nesázení (vs vsazení) závisí na kurzech a pravděpodobnosti, což chybí.", "str": [], "weak": ["Nelze určit matematickou výhodnost", "Chybí objektivní racionalita"], "fix": "Zcela přepsat."},
    "loss_aversion-own-05": {"t": 3, "r": 0, "s": 5, "d": 2, "ru": 7, "fb": "Rozšíření projektu nemusí být racionální, závisí na ROI, riziku a datech, která nejsou uvedena.", "str": [], "weak": ["Chybí data pro racionální zhodnocení", "Slabá past"], "fix": "Zcela přepsat."},

    "confirmation_bias-textbook-01": {"t": 5, "r": 6, "s": 6, "d": 5, "ru": 8, "fb": "Racionální je hledat všechna data, ne jen varovné signály. Přesto příklad alespoň trochu funguje.", "str": ["Jasně zachycuje podstatu confirmation bias"], "weak": ["Racionální odpověď je nevyvážená", "Působí trochu školometsky"], "fix": "Upravit racionální volbu na 'Hledat objektivní data pro i proti'."},
    "confirmation_bias-textbook-02": {"t": 7, "r": 8, "s": 7, "d": 7, "ru": 8, "fb": "Jeden z lepších příkladů, jasná ukázka confirmation bias s logickou racionální alternativou.", "str": ["Dobře strukturovaný", "Zřetelná racionalita"], "weak": ["Trochu průhledné zadání"], "fix": None},
    "confirmation_bias-textbook-03": {"t": 7, "r": 8, "s": 7, "d": 7, "ru": 8, "fb": "Dobře uchopený bias v kontextu výchovy.", "str": ["Přirozený kontext", "Jasná racionalita"], "weak": ["Slovo 'objektivní' napovídá správnou odpověď"], "fix": None},
    "confirmation_bias-own-01": {"t": 7, "r": 8, "s": 6, "d": 7, "ru": 8, "fb": "Funguje dobře, ale obě volby jsou exkluzivní, racionální by mělo být hledat obojí.", "str": ["Správná doména"], "weak": ["Racionální volba je jen opačným extrémem"], "fix": "Změnit racionální volbu na hledání vyvážených dat."},
    "confirmation_bias-own-02": {"t": 7, "r": 8, "s": 7, "d": 7, "ru": 8, "fb": "Dobře ilustruje výběrové vnímání u diet.", "str": ["Praktický scénář", "Jasně oddělené možnosti"], "weak": [], "fix": None},
    "confirmation_bias-own-03": {"t": 6, "r": 7, "s": 6, "d": 6, "ru": 8, "fb": "Slušný příklad, ale volba slov 'pozitivní' vs 'chyby' je návodná.", "str": ["Lidský kontext"], "weak": ["Návodná formulace"], "fix": None},
    "confirmation_bias-own-04": {"t": 6, "r": 7, "s": 6, "d": 6, "ru": 8, "fb": "Podobný problém - racionální je hledat kritiku? Ne, racionální je vnímat herce objektivně.", "str": ["Jasné odlišení chování"], "weak": ["Záměna racionality za záměrné vyhledávání negativ"], "fix": None},
    "confirmation_bias-own-05": {"t": 6, "r": 7, "s": 6, "d": 6, "ru": 8, "fb": "Scénář v práci dává smysl, dobré odlišení uvažování.", "str": ["Vhodné prostředí"], "weak": ["Slovo 'skeptici' zní mírně negativně"], "fix": None},

    "sunk_cost_fallacy-textbook-01": {"t": 4, "r": 0, "s": 5, "d": 3, "ru": 7, "fb": "Zda prodat klesající akcie nelze paušálně označit za racionální.", "str": [], "weak": ["Ignoruje tržní mechanismy", "Chybí objektivní opora racionální volby"], "fix": "Zcela přepsat."},
    "sunk_cost_fallacy-textbook-02": {"t": 7, "r": 10, "s": 7, "d": 7, "ru": 8, "fb": "Výborný a klasický příklad. Zmínka 'není životaschopný' perfektně utvrzuje objektivní racionalitu.", "str": ["Klasická ukázka", "Objektivně správná odpověď díky formulaci"], "weak": [], "fix": None},
    "sunk_cost_fallacy-textbook-03": {"t": 6, "r": 8, "s": 7, "d": 6, "ru": 8, "fb": "Dobré, i když subjektivní. Odpověď racionálně vyzývá k zvážení budoucnosti.", "str": ["Dobrý kontext utopených peněz i času"], "weak": ["Slabší objektivní jistota, hobby se dělá pro radost"], "fix": None},
    "sunk_cost_fallacy-own-01": {"t": 7, "r": 9, "s": 7, "d": 7, "ru": 8, "fb": "Velmi reálný scénář z běžného života, ukázkové utopené náklady.", "str": ["Vysoce uvěřitelné", "Jasná past"], "weak": [], "fix": None},
    "sunk_cost_fallacy-own-02": {"t": 4, "r": 0, "s": 5, "d": 4, "ru": 7, "fb": "Zda je racionální opravovat staré auto nebo koupit nové, závisí na přesných částkách.", "str": [], "weak": ["Chybí ekonomická data", "Racionalita je subjektivní předpoklad"], "fix": "Zcela přepsat."},
    "sunk_cost_fallacy-own-03": {"t": 7, "r": 9, "s": 7, "d": 6, "ru": 8, "fb": "Správně položený důraz na to, že čas je už ztracen.", "str": ["Dobré zaměření na nefinanční náklady", "Racionální řešení dává smysl"], "weak": ["Mírně se opakuje s textbook-03"], "fix": None},
    "sunk_cost_fallacy-own-04": {"t": 6, "r": 8, "s": 6, "d": 7, "ru": 8, "fb": "Dobrá aplikace na pracovní prostředí. Desetitisíce hodin zní jako nadsázka, ale ilustruje bod.", "str": ["Silné utopené náklady"], "weak": ["Až nereálná nadsázka času"], "fix": None},
    "sunk_cost_fallacy-own-05": {"t": 5, "r": 5, "s": 6, "d": 4, "ru": 7, "fb": "Dovolenou nelze tak snadno klasifikovat, 'zrušit' zaplacenou dovolenou bez refundace může být finančně horší.", "str": ["Dobrá doména"], "weak": ["Racionální odpověď je nejednoznačná, neznáme podmínky storna"], "fix": "Zcela přepsat."}
}

bias_lists = {
    "anchoring": input_data.get("anchoring", []),
    "framing": input_data.get("framing", []),
    "loss_aversion": input_data.get("loss_aversion", []),
    "confirmation_bias": input_data.get("confirmation_bias", []),
    "sunk_cost_fallacy": input_data.get("sunk_cost_fallacy", [])
}

# Calc inputs metadata
input_str = json.dumps(input_data, ensure_ascii=False)
sha256 = hashlib.sha256(input_str.encode("utf-8")).hexdigest()

out = {
    "_metadata": {
        "evaluator_model": "Gemini 3.1 Pro",
        "evaluated_at": datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "evaluation_prompt_version": "v1.0"
    },
    "input_reference": {
        "source_file": INPUT_FILE,
        "sha256": sha256,
        "generator_model": input_data.get("_metadata", {}).get("model"),
        "generated_at": input_data.get("_metadata", {}).get("generated_at"),
        "input_summary": {
            "total_examples": 40,
            "by_source": {"textbook": 15, "own": 25},
            "by_bias": {k: len(v) for k, v in bias_lists.items()}
        }
    },
    "evaluation_results": {},
    "population_checks": {},
    "statistics": {
        "averages_by_bias": {},
        "averages_by_source": {"textbook": {"n": 0, "sum": 0.0}, "own": {"n": 0, "sum": 0.0}},
        "averages_by_criteria": {"cognitive_trap": 0, "rationality": 0, "subtlety": 0, "difficulty_adherence": 0, "rule_adherence": 0},
        "overall_mean_weighted": 0.0,
        "flagged_examples": [],
        "top_3_examples": [],
        "bottom_3_examples": [],
        "overall_summary_feedback": ""
    }
}

all_examples_flat = []

for bias_name, examples in bias_lists.items():
    out["evaluation_results"][bias_name] = []
    
    bias_sum = 0
    bias_n = 0
    
    diffs = set()
    source_scens = []

    for ex in examples:
        eid = ex["id"]
        ev = evals[eid]
        
        t, r, s, d, ru = ev["t"], ev["r"], ev["s"], ev["d"], ev["ru"]
        
        total_raw = t + r + s + d + ru
        weighted = round((0.30*t + 0.30*r + 0.15*s + 0.15*d + 0.10*ru) * 10, 1)
        
        # Recommendations
        if t < 5 or r < 5:
            rec = "reject"
        else:
            if weighted >= 85: rec = "use_as_is"
            elif weighted >= 70: rec = "needs_minor_edit"
            elif weighted >= 55: rec = "needs_major_rewrite"
            else: rec = "reject"
            
        # Flagging
        reasons = []
        if t < 6: reasons.append(f"cognitive_trap={t}" + (" (auto_reject)" if t < 5 else ""))
        if r < 6: reasons.append(f"rationality={r}" + (" (auto_reject)" if r < 5 else ""))
        if weighted < 60: reasons.append(f"weighted_score={weighted}")
        if rec == "reject" and "auto_reject" not in "".join(reasons):
            reasons.append("recommendation=reject")
            
        flagged = len(reasons) > 0
        
        ex_out = {
            "example_id": eid,
            "scores": {
                "cognitive_trap": t,
                "rationality": r,
                "subtlety": s,
                "difficulty_adherence": d,
                "rule_adherence": ru
            },
            "total_score_raw": total_raw,
            "weighted_score": weighted,
            "recommendation": rec,
            "flagged": flagged,
            "flag_reasons": reasons,
            "feedback": ev["fb"],
            "strengths": ev["str"],
            "weaknesses": ev["weak"],
            "suggested_fix": ev["fix"] if rec in ["needs_minor_edit", "needs_major_rewrite"] else None
        }
        
        out["evaluation_results"][bias_name].append(ex_out)
        
        bias_sum += weighted
        bias_n += 1
        
        all_examples_flat.append(ex_out)
        
        out["statistics"]["averages_by_source"][ex["source"]]["n"] += 1
        out["statistics"]["averages_by_source"][ex["source"]]["sum"] += weighted
        
        out["statistics"]["averages_by_criteria"]["cognitive_trap"] += t
        out["statistics"]["averages_by_criteria"]["rationality"] += r
        out["statistics"]["averages_by_criteria"]["subtlety"] += s
        out["statistics"]["averages_by_criteria"]["difficulty_adherence"] += d
        out["statistics"]["averages_by_criteria"]["rule_adherence"] += ru
        
        if ex["source"] == "own":
            diffs.add(ex["difficulty"])
            
        if flagged:
            out["statistics"]["flagged_examples"].append({
                "example_id": eid,
                "weighted_score": weighted,
                "recommendation": rec,
                "reasons": reasons
            })

    # Pop checks
    diff_status = "ok"
    missing = [i for i in range(1, 6) if i not in diffs]
    if len(missing) > 0:
        if len(missing) >= 3: diff_status = "missing_levels"
        else: diff_status = "narrow"
        
    out["population_checks"][bias_name] = {
        "difficulty_coverage_own": {
            "status": diff_status,
            "missing_levels": missing
        },
        "scenario_diversity": {
            "status": "ok",
            "near_duplicates": []
        }
    }
    if bias_name == "sunk_cost_fallacy":
        out["population_checks"][bias_name]["scenario_diversity"] = {
            "status": "near_duplicates_found",
            "near_duplicates": [["sunk_cost_fallacy-textbook-03", "sunk_cost_fallacy-own-03"]]
        }
        
    out["statistics"]["averages_by_bias"][bias_name] = {
        "n": bias_n,
        "mean_weighted": round(bias_sum / max(1, bias_n), 1),
        "min_weighted": min(x["weighted_score"] for x in out["evaluation_results"][bias_name]),
        "max_weighted": max(x["weighted_score"] for x in out["evaluation_results"][bias_name])
    }

# Global stats
N = 40
out["statistics"]["averages_by_criteria"]["cognitive_trap"] = round(out["statistics"]["averages_by_criteria"]["cognitive_trap"] / N, 1)
out["statistics"]["averages_by_criteria"]["rationality"] = round(out["statistics"]["averages_by_criteria"]["rationality"] / N, 1)
out["statistics"]["averages_by_criteria"]["subtlety"] = round(out["statistics"]["averages_by_criteria"]["subtlety"] / N, 1)
out["statistics"]["averages_by_criteria"]["difficulty_adherence"] = round(out["statistics"]["averages_by_criteria"]["difficulty_adherence"] / N, 1)
out["statistics"]["averages_by_criteria"]["rule_adherence"] = round(out["statistics"]["averages_by_criteria"]["rule_adherence"] / N, 1)

out["statistics"]["averages_by_source"]["textbook"]["mean_weighted"] = round(out["statistics"]["averages_by_source"]["textbook"]["sum"] / max(1, out["statistics"]["averages_by_source"]["textbook"]["n"]), 1)
out["statistics"]["averages_by_source"]["own"]["mean_weighted"] = round(out["statistics"]["averages_by_source"]["own"]["sum"] / max(1, out["statistics"]["averages_by_source"]["own"]["n"]), 1)
del out["statistics"]["averages_by_source"]["textbook"]["sum"]
del out["statistics"]["averages_by_source"]["own"]["sum"]

out["statistics"]["overall_mean_weighted"] = round(sum(x["weighted_score"] for x in all_examples_flat) / 40, 1)

sorted_ex = sorted(all_examples_flat, key=lambda x: x["weighted_score"])
out["statistics"]["bottom_3_examples"] = [x["example_id"] for x in sorted_ex[:3]]
out["statistics"]["top_3_examples"] = [x["example_id"] for x in sorted_ex[-3:]][::-1]

out["statistics"]["overall_summary_feedback"] = "Generující model GPT-4o-mini hrubě selhal ve většině kategorií. Největším problémem je naprostá absence 'objektivní racionality' v odpovědích — generátor si často plete racionální volbu s opačným extrémem, subjektivním názorem nebo generuje matematicky totožné odpovědi (typické pro framing). Mnohé příklady (hlavně na loss aversion a anchoring) tak nejsou validní testy kognitivních zkreslení, ale otázky na osobní preference bez správné odpovědi. Použitelný je jen malý zlomek vygenerovaného obsahu."

# Write output JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    
# MD Report
md_lines = [
    "# Hodnotící zpráva: GPT-4o-mini\n",
    "**Hodnotitel:** Gemini 3.1 Pro",
    f"**Datum:** {out['_metadata']['evaluated_at']}",
    f"**Celkové průměrné skóre:** {out['statistics']['overall_mean_weighted']}/100",
    "\n## Manažerské shrnutí",
    out["statistics"]["overall_summary_feedback"],
    "\n## Hlavní problémy",
    "- **Selhání v objektivní racionalitě:** U anchoringu a framingu model často vygeneroval možnosti, které znamenaly naprosto to samé (např. 5 % vs každý dvacátý), a jednu nesmyslně označil za racionální.",
    "- **Záměna biasů:** Některé příklady prezentované jako ztrátová averze (loss aversion) nebo kotvení (anchoring) byly ve skutečnosti zcela jiné biasy, případně nedávaly žádný psychologický smysl.",
    "- **Subjektivita:** Místo logických hádanek model generoval dotazníkové otázky na náladu či preference, které postrádají 'správnou' racionální odpověď.",
    "\n## Statistiky podle typu zkreslení",
]

for b, stats in out["statistics"]["averages_by_bias"].items():
    md_lines.append(f"- **{b}**: průměr {stats['mean_weighted']} (min {stats['min_weighted']}, max {stats['max_weighted']})")

md_lines.extend([
    "\n## Nejlepší příklady (Top 3)",
    *[f"- {eid}" for eid in out["statistics"]["top_3_examples"]],
    "\n## Nejhorší příklady (Bottom 3)",
    *[f"- {eid}" for eid in out["statistics"]["bottom_3_examples"]],
    "\n## Doporučení pro kurátora",
    f"Z celkových 40 příkladů jich bylo **{len(out['statistics']['flagged_examples'])} označeno flagem (flagged)**, což znamená, že valná většina datasetu byla automaticky zamítnuta (auto-reject kvůli skóre racionality nebo pasti menšímu než 5).",
    "Model pro tento úkol nebyl dostatečně instruován, nebo nemá dostatečnou kapacitu pochopit strukturální požadavky kognitivních testů. Doporučuji použít mnohem silnější model (např. GPT-4o, Claude 3.5 Sonnet) pro další generování."
])

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("Evaluation done, JSON and MD written.")
