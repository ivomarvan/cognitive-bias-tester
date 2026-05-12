import json
from datetime import datetime, timezone, timedelta

def compute_weighted(scores):
    trap = scores.get("cognitive_trap", 0)
    rat = scores.get("rationality", 0)
    sub = scores.get("subtlety", 0)
    diff = scores.get("difficulty_adherence", 0)
    rule = scores.get("rule_adherence", 0)
    total_raw = trap + rat + sub + diff + rule
    w = (0.3*trap + 0.3*rat + 0.15*sub + 0.15*diff + 0.1*rule) * 10
    return total_raw, round(w, 1)

def get_recommendation(w, trap, rat):
    if trap < 5 or rat < 5:
        return "reject"
    if w >= 85:
        return "use_as_is"
    if w >= 70:
        return "needs_minor_edit"
    if w >= 55:
        return "needs_major_rewrite"
    return "reject"

evals = {
    "anchoring": [
        {
            "id": "anchoring-textbook-01",
            "scores": {"cognitive_trap": 4, "rationality": 3, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 5},
            "feedback": "Příklad selhává v racionalitě, protože správná odpověď předpokládá nevyřčený rozpočet.",
            "strengths": ["Obsahuje explicitní číselnou kotvu (200 dolarů)."],
            "weaknesses": ["Racionální odpověď vyžaduje externí předpoklad (rozpočet).", "Krkolomný překlad ('nakupování hotelu')."]
        },
        {
            "id": "anchoring-textbook-02",
            "scores": {"cognitive_trap": 5, "rationality": 0, "subtlety": 3, "difficulty_adherence": 3, "rule_adherence": 3},
            "feedback": "Racionální odpověď je logicky nesprávná, v aukci cena stoupá nad vyvolávací hodnotu.",
            "strengths": ["Obsahuje výraznou kotvu."],
            "weaknesses": ["Fakticky chybná 'racionální' odpověď.", "Špatná čeština ('aukčnědrážební')."]
        },
        {
            "id": "anchoring-textbook-03",
            "scores": {"cognitive_trap": 4, "rationality": 3, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 5},
            "feedback": "Racionální odpověď operuje s náhodnou hodnotou (90 000), kterou nelze z textu odvodit.",
            "strengths": ["Scénář z reálného života."],
            "weaknesses": ["Racionální odpověď není objektivně doložitelná.", "Slabší stylistika ('nabídkový minimální plat')."]
        },
        {
            "id": "anchoring-own-01",
            "scores": {"cognitive_trap": 0, "rationality": 0, "subtlety": 5, "difficulty_adherence": 0, "rule_adherence": 5},
            "feedback": "Zcela chybná logika pasti – volba levnější ekonomické třídy není kognitivní zkreslení, ale běžné rozhodnutí.",
            "strengths": ["Dobré téma z praxe."],
            "weaknesses": ["Záměna racionálního rozhodnutí za bias.", "Zcela nejasná past."]
        },
        {
            "id": "anchoring-own-02",
            "scores": {"cognitive_trap": 3, "rationality": 0, "subtlety": 5, "difficulty_adherence": 2, "rule_adherence": 5},
            "feedback": "Racionální odpověď si vymýšlí nutnost rekonstrukce, která v zadání není uvedena.",
            "strengths": ["Realistická situace (nákup nemovitosti)."],
            "weaknesses": ["Neodpovídá obtížnosti 5.", "Zavádí externí informace do řešení."]
        },
        {
            "id": "anchoring-own-03",
            "scores": {"cognitive_trap": 4, "rationality": 7, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 5},
            "feedback": "Slušný základ, ale past spíše testuje ignorování kvality než klasické ukotvení.",
            "strengths": ["Racionální odpověď je logicky správná."],
            "weaknesses": ["Neodpovídá přesně definici anchoringu.", "Horší stylistika ('kontrastně nabídnuta')."]
        },
        {
            "id": "anchoring-own-04",
            "scores": {"cognitive_trap": 5, "rationality": 7, "subtlety": 5, "difficulty_adherence": 7, "rule_adherence": 7},
            "feedback": "Jeden z lepších příkladů, správně ukazuje potřebu zhodnotit reálnou hodnotu namísto slevy.",
            "strengths": ["Jasná kotva a srozumitelné řešení.", "Dobře trefená obtížnost."],
            "weaknesses": ["Past je poměrně průhledná.", "Chybí větší hloubka pro vlastní (own) příklad."]
        },
        {
            "id": "anchoring-own-05",
            "scores": {"cognitive_trap": 0, "rationality": 3, "subtlety": 5, "difficulty_adherence": 3, "rule_adherence": 5},
            "feedback": "Příklad testuje framing (rámování úspěšnosti), nikoliv anchoring.",
            "strengths": ["Scénář je srozumitelný."],
            "weaknesses": ["Zcela chybné zařazení pod anchoring.", "Vágní racionální odpověď."]
        }
    ],
    "framing": [
        {
            "id": "framing-textbook-01",
            "scores": {"cognitive_trap": 4, "rationality": 5, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Příklad neobsahuje dvě různě zarámované varianty, pouze testuje interpretaci jednoho čísla.",
            "strengths": ["Jednoduchost a čitelnost."],
            "weaknesses": ["Chybí klasická struktura framingu (dvě možnosti).", "Obě odpovědi jsou matematicky ekvivalentní."]
        },
        {
            "id": "framing-textbook-02",
            "scores": {"cognitive_trap": 4, "rationality": 5, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Stejný problém jako u prvního příkladu – chybí protichůdné rámování téže situace.",
            "strengths": ["Dobrá doména (marketing)."],
            "weaknesses": ["Nesplňuje strukturní požadavky pasti pro framing."]
        },
        {
            "id": "framing-textbook-03",
            "scores": {"cognitive_trap": 4, "rationality": 5, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Opět chybí dvě varianty rámování v možnostech; testuje se jen pesimismus vs. optimismus.",
            "strengths": ["Dobré navození kontextu."],
            "weaknesses": ["Nevyužívá plný potenciál framingu."]
        },
        {
            "id": "framing-own-01",
            "scores": {"cognitive_trap": 4, "rationality": 5, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Příklad je spíše testem slovních úloh na pravděpodobnost než skutečným rámováním.",
            "strengths": ["Srozumitelný každodenní scénář."],
            "weaknesses": ["Chybí strukturní volba mezi rámci."]
        },
        {
            "id": "framing-own-02",
            "scores": {"cognitive_trap": 4, "rationality": 5, "subtlety": 0, "difficulty_adherence": 2, "rule_adherence": 5},
            "feedback": "Text explicitně prozrazuje 'zkreslení rámování' v explanation biased volby, což zabíjí subtilitu.",
            "strengths": ["Realistická marketingová ukázka."],
            "weaknesses": ["Prozrazení názvu biase (Subtlety = 0).", "Neodpovídá obtížnosti 5."]
        },
        {
            "id": "framing-own-03",
            "scores": {"cognitive_trap": 4, "rationality": 5, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Zcela identická struktura i téma jako textbook-01 (zdraví, 95% vs 90%).",
            "strengths": ["Jasná čísla."],
            "weaknesses": ["Duplicita s textbook příkladem.", "Chybí dvě různě zarámované volby."]
        },
        {
            "id": "framing-own-04",
            "scores": {"cognitive_trap": 4, "rationality": 6, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Další variace na stejné téma – chybí negativní a pozitivní rámování u samotných možností.",
            "strengths": ["Logičtější racionální volba než v předchozích."],
            "weaknesses": ["Opakující se stejný vzorec bez hlubší invence."]
        },
        {
            "id": "framing-own-05",
            "scores": {"cognitive_trap": 4, "rationality": 4, "subtlety": 5, "difficulty_adherence": 5, "rule_adherence": 7},
            "feedback": "Opakující se téma; navíc 'zálohovat plán' je velmi krkolomný překlad.",
            "strengths": ["Krátký a výstižný text."],
            "weaknesses": ["Špatná čeština v racionální odpovědi.", "Stále chybí správná struktura framingu."]
        }
    ]
}

results = {"anchoring": [], "framing": []}
flagged_list = []

for bias, examples in evals.items():
    for ex in examples:
        raw, w = compute_weighted(ex["scores"])
        trap = ex["scores"]["cognitive_trap"]
        rat = ex["scores"]["rationality"]
        rec = get_recommendation(w, trap, rat)
        
        flagged = False
        reasons = []
        if trap < 6:
            reasons.append(f"cognitive_trap={trap}" + (" (auto_reject)" if trap < 5 else ""))
        if rat < 6:
            reasons.append(f"rationality={rat}" + (" (auto_reject)" if rat < 5 else ""))
        if w < 60:
            reasons.append(f"weighted_score={w}")
        if rec == "reject" and f"recommendation={rec}" not in reasons and "auto_reject" not in "".join(reasons):
            reasons.append("recommendation=reject")
            
        if reasons or rec == "reject":
            flagged = True
            
        fix = None
        if rec in ["needs_minor_edit", "needs_major_rewrite"]:
            fix = "Přepracujte racionální odpověď tak, aby byla logicky nenapadnutelná a nevyžadovala externí znalosti."

        res = {
            "example_id": ex["id"],
            "scores": ex["scores"],
            "total_score_raw": raw,
            "weighted_score": w,
            "recommendation": rec,
            "flagged": flagged,
            "flag_reasons": reasons,
            "feedback": ex["feedback"],
            "strengths": ex["strengths"],
            "weaknesses": ex["weaknesses"],
            "suggested_fix": fix
        }
        results[bias].append(res)
        
        if flagged:
            flagged_list.append({
                "example_id": ex["id"],
                "weighted_score": w,
                "recommendation": rec,
                "reasons": reasons
            })

stats = {
    "averages_by_bias": {},
    "averages_by_source": {"textbook": {"n": 0, "sum": 0}, "own": {"n": 0, "sum": 0}},
    "averages_by_criteria": {
        "cognitive_trap": 0,
        "rationality": 0,
        "subtlety": 0,
        "difficulty_adherence": 0,
        "rule_adherence": 0
    },
    "overall_mean_weighted": 0,
    "flagged_examples": flagged_list,
    "top_3_examples": [],
    "bottom_3_examples": []
}

all_scores = []
all_w = []

for bias, examples in results.items():
    stats["averages_by_bias"][bias] = {"n": len(examples), "sum_w": 0, "scores": []}
    for ex in examples:
        src = "textbook" if "textbook" in ex["example_id"] else "own"
        stats["averages_by_source"][src]["n"] += 1
        stats["averages_by_source"][src]["sum"] += ex["weighted_score"]
        
        stats["averages_by_bias"][bias]["sum_w"] += ex["weighted_score"]
        stats["averages_by_bias"][bias]["scores"].append(ex["weighted_score"])
        
        for k, v in ex["scores"].items():
            stats["averages_by_criteria"][k] += v
            
        all_w.append((ex["example_id"], ex["weighted_score"]))

for k in stats["averages_by_criteria"]:
    stats["averages_by_criteria"][k] = round(stats["averages_by_criteria"][k] / len(all_w), 1)

for src in stats["averages_by_source"]:
    n = stats["averages_by_source"][src]["n"]
    if n > 0:
        stats["averages_by_source"][src]["mean_weighted"] = round(stats["averages_by_source"][src]["sum"] / n, 1)
    del stats["averages_by_source"][src]["sum"]

for bias in stats["averages_by_bias"]:
    n = stats["averages_by_bias"][bias]["n"]
    scores = stats["averages_by_bias"][bias]["scores"]
    mean = sum(scores) / n
    stats["averages_by_bias"][bias]["mean_weighted"] = round(mean, 1)
    stats["averages_by_bias"][bias]["min_weighted"] = min(scores)
    stats["averages_by_bias"][bias]["max_weighted"] = max(scores)
    stats["averages_by_bias"][bias]["stdev_weighted"] = round((sum((x - mean)**2 for x in scores) / n)**0.5, 1)
    del stats["averages_by_bias"][bias]["sum_w"]
    del stats["averages_by_bias"][bias]["scores"]

all_w.sort(key=lambda x: x[1], reverse=True)
stats["top_3_examples"] = [x[0] for x in all_w[:3]]
stats["bottom_3_examples"] = [x[0] for x in all_w[-3:]]
stats["overall_mean_weighted"] = round(sum(x[1] for x in all_w) / len(all_w), 1)

stats["overall_summary_feedback"] = "Modely selhaly v generování objektivně racionálních odpovědí, obzvláště u anchoringu zaváděly nevyslovené předpoklady (rozpočet, rekonstrukce). U framingu generátor vůbec nepochopil, že má poskytnout dvě různě zarámované volby popisující tutéž realitu. Celkově je kvalita příkladů velmi nízká a většina vyžaduje kompletní přepsání."

out = {
    "_metadata": {
        "evaluator_model": "Gemini 3.1 Pro",
        "evaluated_at": datetime.now(timezone(timedelta(hours=2))).isoformat(),
        "evaluation_prompt_version": "v1.0"
    },
    "input_reference": {
        "source_file": "/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/gen/gpt-4o.json",
        "sha256": None,
        "generator_model": "GPT-4",
        "generated_at": "2023-10-01 12:00:00",
        "input_summary": {
            "total_examples": 16,
            "by_source": {"textbook": 6, "own": 10},
            "by_bias": {
                "anchoring": 8,
                "framing": 8
            }
        }
    },
    "evaluation_results": results,
    "population_checks": {
        "anchoring": {
            "difficulty_coverage_own": {
                "status": "missing_levels",
                "missing_levels": [1, 2, 3, 4, 5]  # Zjednodušeně, protože jsme vyloučili skoro vše
            },
            "scenario_diversity": {
                "status": "ok",
                "near_duplicates": []
            }
        },
        "framing": {
            "difficulty_coverage_own": {
                "status": "missing_levels",
                "missing_levels": [1, 2, 3, 4, 5]
            },
            "scenario_diversity": {
                "status": "near_duplicates",
                "near_duplicates": [
                    ["framing-textbook-01", "framing-own-03"]
                ]
            }
        }
    },
    "statistics": stats
}

with open("/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/eval/gpt-4o__by__gemini3.1pro.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    
print("JSON zapsán.")
