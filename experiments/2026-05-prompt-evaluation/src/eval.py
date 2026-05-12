#!/usr/bin/env python3
"""Evaluate Case generation + judge prompts across multiple LLM models.

Prompt definitions live in data/v1-plain/prompts/prompts-v<VERSION>.json.
The script auto-selects the highest available version unless --prompt-version is given.
The prompt file is copied into the run output directory for full reproducibility.

For each (model, bias_type, variant) combination:
  1. Calls the generation prompt → parses JSON Case
  2. Feeds the Case to the judge prompt → pass/fail + score
  3. Saves raw API responses and generates a Markdown report

Output structure:
  data/eval-runs/<YYYYMMDD_HHMMSS>_<git-hash>/
    run_meta.json            — inputs, git state, prompt version
    prompts-v<VERSION>.json  — copy of the prompt file used (for reproducibility)
    raw/<model>/
      <bias>_v<N>_gen.json
      <bias>_v<N>_judge.json
    report.md                — human-readable case-by-case comparison
    summary.json             — scores + costs only (easy cross-run comparison)

Usage (run from experiments/2026-05-prompt-evaluation/):
  pip install -r src/requirements.txt
  # API keys are loaded from .env in the project root (or set in shell):
  #   OPENAI_API_KEY   — required for gpt-4o-mini / gpt-4o
  #   GOOGLE_API_KEY   — optional, for Gemini models
  #   ANTHROPIC_API_KEY — optional, for Claude models

  python src/eval.py                                           # defaults: gpt-4o-mini, 2 variants, English
  python src/eval.py --models gpt-4o-mini,gemini-2.0-flash    # compare two models
  python src/eval.py --variants 3 --lang cs                   # Czech output, 3 variants
  python src/eval.py --bias anchoring,framing                 # only two bias types
  python src/eval.py --prompt-version 1.1.0                   # use a specific prompt version
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

_SCRIPT_DIR = Path(__file__).resolve().parent          # experiments/.../src/
_EXPERIMENT_DIR = _SCRIPT_DIR.parent                    # experiments/2026-05-prompt-evaluation/
_PROJECT_ROOT = _EXPERIMENT_DIR.parent.parent           # project root
# Keys already set in the shell environment take precedence over .env values.
load_dotenv(_PROJECT_ROOT / ".env")

# ── Bias types (MVP set) ──────────────────────────────────────────────────────

BIAS_TYPES: list[dict[str, str]] = [
    {"slug": "anchoring", "name": "Anchoring (Ukotvení)"},
    {"slug": "framing", "name": "Framing (Rámování)"},
    {"slug": "loss_aversion", "name": "Loss Aversion (Averze ke ztrátě)"},
    {"slug": "confirmation_bias", "name": "Confirmation Bias (Konfirmační zkreslení)"},
    {"slug": "sunk_cost_fallacy", "name": "Sunk Cost Fallacy (Klam utopených nákladů)"},
]

# ── Prompt loading ────────────────────────────────────────────────────────────

_PROMPTS_DIR = _EXPERIMENT_DIR / "data" / "v1-plain" / "prompts"


def _available_versions() -> list[str]:
    """Return all prompt versions found in the prompts/ directory, sorted ascending."""
    files = sorted(_PROMPTS_DIR.glob("prompts-v*.json"))
    versions = []
    for f in files:
        # Extract version from filename: prompts-v1.0.0.json → "1.0.0"
        stem = f.stem  # "prompts-v1.0.0"
        if stem.startswith("prompts-v"):
            versions.append(stem[len("prompts-v"):])
    return versions


def load_prompts(version: str | None = None) -> tuple[dict[str, Any], Path]:
    """Load prompt definitions from prompts/prompts-v<VERSION>.json.

    Args:
        version: Specific version string (e.g. "1.0.0"). None = use highest available.

    Returns:
        Tuple of (prompts dict, source Path).

    Raises:
        FileNotFoundError: if no prompt files exist or the requested version is missing.
    """
    available = _available_versions()
    if not available:
        raise FileNotFoundError(f"No prompt files found in {_PROMPTS_DIR}")

    if version is None:
        selected = available[-1]  # highest version (lexicographic, works for vMAJOR.MINOR.PATCH)
    elif version in available:
        selected = version
    else:
        raise FileNotFoundError(
            f"Prompt version {version!r} not found. Available: {available}"
        )

    prompt_file = _PROMPTS_DIR / f"prompts-v{selected}.json"
    data = json.loads(prompt_file.read_text(encoding="utf-8"))
    return data, prompt_file


def render(template: str, **kwargs: Any) -> str:
    """Fill {variable} placeholders in a user_template string.

    Only user_template fields are rendered — system prompts are used as-is.
    """
    return template.format(**kwargs)


# ── Cost table (USD per 1M tokens, update as pricing changes) ────────────────

_COST_PER_1M: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
}


def estimate_cost(model: str, usage: dict[str, int]) -> float:
    prices = _COST_PER_1M.get(model, {"input": 0.0, "output": 0.0})
    return (
        usage.get("prompt_tokens", 0) * prices["input"] / 1_000_000
        + usage.get("completion_tokens", 0) * prices["output"] / 1_000_000
    )


# ── Model callers ─────────────────────────────────────────────────────────────


def _provider(model: str) -> str:
    if model.startswith(("gpt-", "o1", "o3")):
        return "openai"
    if model.startswith("gemini"):
        return "gemini"
    if model.startswith("claude"):
        return "anthropic"
    raise ValueError(f"Cannot determine provider for model: {model!r}")


def _call_openai(messages: list[dict[str, str]], model: str) -> tuple[str, dict[str, int]]:
    from openai import OpenAI

    resp = OpenAI().chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        response_format={"type": "json_object"},
        timeout=60,
        max_tokens=4096,   # eval responses are short; 4096 sufficient
    )
    usage = {
        "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
        "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
    }
    return resp.choices[0].message.content or "", usage


def _call_gemini(messages: list[dict[str, str]], model: str) -> tuple[str, dict[str, int]]:
    """Call Gemini using the current google-genai SDK (replaces deprecated google.generativeai)."""
    from google import genai  # type: ignore[import-untyped]
    from google.genai import types  # type: ignore[import-untyped]

    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    user = next((m["content"] for m in messages if m["role"] == "user"), "")

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        max_output_tokens=4096,
        system_instruction=system or None,
    )
    resp = client.models.generate_content(model=model, contents=user, config=config)
    usage = {
        "prompt_tokens": getattr(resp.usage_metadata, "prompt_token_count", 0),
        "completion_tokens": getattr(resp.usage_metadata, "candidates_token_count", 0),
    }
    return resp.text, usage


def _call_anthropic(
    messages: list[dict[str, str]], model: str
) -> tuple[str, dict[str, int]]:
    import anthropic  # type: ignore[import-untyped]

    client = anthropic.Anthropic()
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    user_msgs = [m for m in messages if m["role"] != "system"]
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=user_msgs,  # type: ignore[arg-type]
    )
    usage = {
        "prompt_tokens": resp.usage.input_tokens,
        "completion_tokens": resp.usage.output_tokens,
    }
    return resp.content[0].text, usage  # type: ignore[attr-defined]


_CALLERS = {
    "openai": _call_openai,
    "gemini": _call_gemini,
    "anthropic": _call_anthropic,
}

# ── Git helpers ───────────────────────────────────────────────────────────────


def _git_hash() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


def _git_dirty() -> bool:
    try:
        return bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return False


# ── Core evaluation ───────────────────────────────────────────────────────────


def evaluate_one(
    model: str,
    bias: dict[str, str],
    variant: int,
    lang: str,
    raw_dir: Path,
    prompts: dict[str, Any],
) -> dict[str, Any]:
    """Run one generation + judge cycle; return result dict."""
    slug = bias["slug"]
    model_dir = raw_dir / model.replace("/", "-")
    model_dir.mkdir(parents=True, exist_ok=True)

    caller = _CALLERS[_provider(model)]
    result: dict[str, Any] = {
        "model": model,
        "bias_slug": slug,
        "bias_name": bias["name"],
        "variant": variant,
        "gen_ok": False,
        "judge_ok": False,
        "judge_pass": None,
        "judge_score": None,
        "judge_reasoning": None,
        "cost_usd": 0.0,
        "case": None,
        "errors": [],
    }

    # ── Step 1: Generation ────────────────────────────────────────────────────
    gen_file = model_dir / f"{slug}_v{variant}_gen.json"
    gen_messages = [
        {"role": "system", "content": prompts["generator"]["system"]},
        {
            "role": "user",
            "content": render(
                prompts["generator"]["user_template"],
                bias_name=bias["name"],
                variant=variant,
                lang=lang,
            ),
        },
    ]
    gen_content = ""
    try:
        gen_content, gen_usage = caller(gen_messages, model)
        gen_file.write_text(
            json.dumps(
                {"content": gen_content, "usage": gen_usage}, ensure_ascii=False, indent=2
            )
        )
        case_obj = json.loads(gen_content)
        result["gen_ok"] = True
        result["cost_usd"] += estimate_cost(model, gen_usage)
        result["case"] = case_obj
    except json.JSONDecodeError as exc:
        result["errors"].append(f"gen JSON parse: {exc}")
        gen_file.write_text(
            json.dumps(
                {"content": gen_content, "error": str(exc)}, ensure_ascii=False, indent=2
            )
        )
        return result
    except Exception as exc:
        result["errors"].append(f"gen API: {exc}")
        return result

    # ── Step 2: Judge ─────────────────────────────────────────────────────────
    judge_file = model_dir / f"{slug}_v{variant}_judge.json"
    judge_messages = [
        {"role": "system", "content": prompts["judge"]["system"]},
        {
            "role": "user",
            "content": render(
                prompts["judge"]["user_template"],
                bias_name=bias["name"],
                case_json=json.dumps(case_obj, ensure_ascii=False),
            ),
        },
    ]
    judge_content = ""
    try:
        judge_content, judge_usage = caller(judge_messages, model)
        judge_file.write_text(
            json.dumps(
                {"content": judge_content, "usage": judge_usage}, ensure_ascii=False, indent=2
            )
        )
        judge_obj = json.loads(judge_content)
        result["judge_ok"] = True
        result["judge_pass"] = judge_obj.get("pass")
        result["judge_score"] = judge_obj.get("score")
        result["judge_reasoning"] = judge_obj.get("reasoning", "")
        result["cost_usd"] += estimate_cost(model, judge_usage)
    except json.JSONDecodeError as exc:
        result["errors"].append(f"judge JSON parse: {exc}")
        judge_file.write_text(
            json.dumps(
                {"content": judge_content, "error": str(exc)}, ensure_ascii=False, indent=2
            )
        )
    except Exception as exc:
        result["errors"].append(f"judge API: {exc}")

    return result


# ── Report generation ─────────────────────────────────────────────────────────

_OPTION_LABELS = "ABCD"


def _render_case(case: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    lines.append(f"**{case.get('title', '—')}**")
    lines.append("")
    lines.append(f"> {case.get('question', '—')}")
    lines.append("")
    correct_idx: int = case.get("correct_option", -1)
    for i, opt in enumerate(case.get("options", [])):
        marker = " ✅" if i == correct_idx else ""
        lines.append(
            f"- **{opt.get('label', _OPTION_LABELS[i])}**{marker}: {opt.get('text', '')}"
        )
    lines.append("")
    lines.append(f"*Explanation:* {case.get('explanation', '—')}")
    return lines


def generate_report(
    results: list[dict[str, Any]], run_dir: Path, meta: dict[str, Any]
) -> None:
    lines = [
        "# Prompt Evaluation Report",
        "",
        f"**Run:** `{meta['run_id']}`  ",
        f"**Git:** `{meta['git_hash']}`{'  ⚠ uncommitted changes' if meta['git_dirty'] else ''}  ",
        f"**Prompt:** `{meta['prompt_file']}` (v{meta['prompt_version']})  ",
        f"**Models:** {', '.join(f'`{m}`' for m in meta['models'])}  ",
        f"**Language:** `{meta['language']}`  ",
        f"**Variants per bias:** {meta['variants_per_bias']}  ",
        "",
        "---",
        "",
    ]

    by_bias: dict[str, list[dict[str, Any]]] = {}
    for r in results:
        by_bias.setdefault(r["bias_slug"], []).append(r)

    for slug, bias_results in by_bias.items():
        lines.append(f"## {bias_results[0]['bias_name']}")
        lines.append("")
        for r in bias_results:
            score_str = f"{r['judge_score']:.2f}" if r["judge_score"] is not None else "—"
            icon = "⚠️" if r["errors"] else ("✅" if r.get("judge_pass") else "❌")
            lines.append(
                f"### `{r['model']}` | variant {r['variant']}  {icon}  score={score_str}"
            )
            lines.append("")
            if r["case"]:
                lines.extend(_render_case(r["case"]))
                lines.append("")
            if r["judge_ok"]:
                lines.append(f"**Judge:** {r['judge_reasoning']}")
            if r["errors"]:
                lines.append(f"**Errors:** {'; '.join(r['errors'])}")
            lines.append(f"**Cost:** ${r['cost_usd']:.5f}")
            lines.append("")
            lines.append("---")
            lines.append("")

    total_cost = sum(r["cost_usd"] for r in results)
    pass_count = sum(1 for r in results if r.get("judge_pass"))
    fail_count = sum(1 for r in results if r["judge_ok"] and not r.get("judge_pass"))
    error_count = sum(1 for r in results if r["errors"])

    lines += [
        "## Summary table",
        "",
        "| Model | Bias | Var | Pass | Score | Cost USD |",
        "|-------|------|-----|------|-------|----------|",
    ]
    for r in results:
        icon = "⚠️" if r["errors"] else ("✅" if r.get("judge_pass") else "❌")
        score_str = f"{r['judge_score']:.2f}" if r["judge_score"] is not None else "—"
        lines.append(
            f"| `{r['model']}` | {r['bias_slug']} | {r['variant']} "
            f"| {icon} | {score_str} | ${r['cost_usd']:.5f} |"
        )
    lines += [
        "",
        f"**Pass: {pass_count} / Fail: {fail_count} / Error: {error_count}**  ",
        f"**Total cost: ${total_cost:.4f}**",
    ]

    (run_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")

    summary = {
        "run_id": meta["run_id"],
        "prompt_version": meta["prompt_version"],
        "total_cost_usd": round(total_cost, 5),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "error_count": error_count,
        "results": [
            {
                "model": r["model"],
                "bias_slug": r["bias_slug"],
                "variant": r["variant"],
                "judge_pass": r.get("judge_pass"),
                "judge_score": r.get("judge_score"),
                "cost_usd": round(r["cost_usd"], 6),
                "errors": r["errors"],
            }
            for r in results
        ],
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── Main ──────────────────────────────────────────────────────────────────────

_ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


def main() -> None:
    available_versions = _available_versions()
    version_hint = (
        f"available: {available_versions}" if available_versions else "none found"
    )

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--models", default="gpt-4o-mini", help="Comma-separated model names")
    parser.add_argument(
        "--variants", type=int, default=2, help="Variants per bias type (default: 2)"
    )
    parser.add_argument(
        "--lang", default="en", choices=["en", "cs"], help="Output language (default: en)"
    )
    parser.add_argument(
        "--bias", default=None, help="Comma-separated bias slugs to test (default: all 5)"
    )
    parser.add_argument(
        "--prompt-version",
        default=None,
        metavar="VERSION",
        help=f"Prompt version to use (default: highest). {version_hint}",
    )
    parser.add_argument(
        "--list-prompts",
        action="store_true",
        help="List available prompt versions and exit",
    )
    args = parser.parse_args()

    if args.list_prompts:
        print("Available prompt versions:")
        for v in available_versions:
            marker = " ← (latest)" if v == available_versions[-1] else ""
            print(f"  {v}{marker}")
        return

    # Load prompts
    try:
        prompts, prompt_file = load_prompts(args.prompt_version)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    # Validate models against available API keys
    requested_models = [m.strip() for m in args.models.split(",")]
    models = []
    for model in requested_models:
        key = _ENV_KEYS.get(_provider(model), "")
        if not os.environ.get(key):
            print(f"⚠  {key} not set — skipping {model}")
        else:
            models.append(model)
    if not models:
        print("No models available. Set at least OPENAI_API_KEY.")
        sys.exit(1)

    # Select bias types
    selected_biases = BIAS_TYPES
    if args.bias:
        slugs = {s.strip() for s in args.bias.split(",")}
        selected_biases = [b for b in BIAS_TYPES if b["slug"] in slugs]
        if not selected_biases:
            print(f"No matching slugs. Available: {[b['slug'] for b in BIAS_TYPES]}")
            sys.exit(1)

    # Set up run output directory
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"{ts}_{_git_hash()}"
    run_dir = _EXPERIMENT_DIR / "data" / "eval-runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Copy prompt file into run directory for reproducibility
    shutil.copy2(prompt_file, run_dir / prompt_file.name)

    meta: dict[str, Any] = {
        "run_id": run_id,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "git_hash": _git_hash(),
        "git_dirty": _git_dirty(),
        "models": models,
        "bias_slugs": [b["slug"] for b in selected_biases],
        "variants_per_bias": args.variants,
        "language": args.lang,
        "prompt_version": prompts["version"],
        "prompt_file": prompt_file.name,
    }
    (run_dir / "run_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_calls = len(models) * len(selected_biases) * args.variants * 2
    print(f"\nRun ID   : {run_id}")
    print(f"Prompts  : {prompt_file.name}  (v{prompts['version']})")
    print(f"Models   : {models}")
    print(f"Biases   : {[b['slug'] for b in selected_biases]}")
    print(f"Variants : {args.variants}   Lang: {args.lang}   API calls: {total_calls}\n")

    results: list[dict[str, Any]] = []
    raw_dir = run_dir / "raw"

    for model in models:
        for bias in selected_biases:
            for variant in range(args.variants):
                label = f"{model:30s}  {bias['slug']:22s}  v{variant}"
                print(f"  → {label} ...", end=" ", flush=True)
                r = evaluate_one(model, bias, variant, args.lang, raw_dir, prompts)
                results.append(r)
                if r["errors"]:
                    print(f"ERROR  {r['errors']}")
                else:
                    icon = "✅" if r.get("judge_pass") else "❌"
                    score = r["judge_score"]
                    print(f"{icon}  score={score:.2f}  ${r['cost_usd']:.5f}")

    generate_report(results, run_dir, meta)

    total_cost = sum(r["cost_usd"] for r in results)
    pass_count = sum(1 for r in results if r.get("judge_pass"))
    print(f"\n{'─'*60}")
    print(f"Pass: {pass_count}/{len(results)}   Total cost: ${total_cost:.4f}")
    print(f"Output  : {run_dir}/")
    print(f"Report  : {run_dir}/report.md\n")


if __name__ == "__main__":
    main()
