#!/usr/bin/env python3
"""ALG1 pipeline — evaluate LLM prompts for cognitive bias example generation.

Algorithm:
  gen:    P1(gen_prompt) → M1 → json1          (generation step)
  eval:   P2(eval_prompt) + json1 → M2 → json2 (evaluation step)
  report: all json2 files → report.html        (aggregation)

Output files (relative to experiment root):
  data/<RUN_NAME>/results/gen/<m1-slug>.json
  data/<RUN_NAME>/results/eval/<m1-slug>__by__<m2-slug>.json
  data/<RUN_NAME>/results/report.html

Usage (run from experiments/2026-05-prompt-evaluation/):
  python src/pipeline.py gen  --model gpt-4o-mini
  python src/pipeline.py eval --gen-model gpt-4o-mini --eval-model gpt-4o
  python src/pipeline.py report
  python src/pipeline.py models          # list API-accessible models + status
  python src/pipeline.py list            # list all gen/eval files found

To work with a different run, change _RUN_NAME below.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

_SCRIPT_DIR = Path(__file__).resolve().parent          # experiments/.../src/
_EXPERIMENT_DIR = _SCRIPT_DIR.parent                    # experiments/2026-05-prompt-evaluation/
_PROJECT_ROOT = _EXPERIMENT_DIR.parent.parent           # project root
load_dotenv(_PROJECT_ROOT / ".env")

# ── Paths ─────────────────────────────────────────────────────────────────────

# Active run — change _RUN_NAME to switch to a different experiment run.
_RUN_NAME = "v1-plain"
_RUN_DIR = _EXPERIMENT_DIR / "data" / _RUN_NAME
_PROMPTS_DIR = _RUN_DIR / "prompts"
_GEN_PROMPT_FILE = _PROMPTS_DIR / "prompt_for_examples.md"
_EVAL_PROMPT_FILE = _PROMPTS_DIR / "prompt_for_evaluating_generated_examples.md"

_OUTPUT_DIR = _RUN_DIR / "results"
_GEN_DIR = _OUTPUT_DIR / "gen"
_EVAL_DIR = _OUTPUT_DIR / "eval"

# ── Known API models ──────────────────────────────────────────────────────────
# Extend as new API models become available.

_API_MODELS: dict[str, str] = {
    # slug → provider
    "gpt-4o-mini": "openai",
    "gpt-4o": "openai",
    "gpt-4.5-preview": "openai",
    "gemini-2.0-flash": "gemini",
    "gemini-1.5-flash": "gemini",
    "gemini-2.5-pro": "gemini",
    "claude-3-5-haiku-20241022": "anthropic",
    "claude-3-5-sonnet-20241022": "anthropic",
    "claude-sonnet-4-6": "anthropic",
}

_ENV_KEYS: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}

# ── Model callers ─────────────────────────────────────────────────────────────


def _call_openai(system: str, user: str, model: str) -> str:
    from openai import OpenAI

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    resp = OpenAI().chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        response_format={"type": "json_object"},
        timeout=300,
        max_tokens=16384,   # generation produces ~10-14k tokens; 8192 caused truncation
    )
    return resp.choices[0].message.content or ""


def _call_gemini(system: str, user: str, model: str) -> str:
    """Call Gemini using the current google-genai SDK (replaces deprecated google.generativeai)."""
    import time
    from google import genai  # type: ignore[import-untyped]
    from google.genai import types  # type: ignore[import-untyped]

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        max_output_tokens=16384,
        system_instruction=system or None,
    )

    # Retry once on 429 quota errors (free-tier per-minute limits recover in ~30 s)
    for attempt in range(2):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=user,
                config=config,
            )
            return resp.text
        except Exception as exc:
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                if attempt == 0:
                    wait = 35
                    print(f"\n  ⚠  Gemini 429 quota — waiting {wait}s before retry...")
                    time.sleep(wait)
                    continue
                # Second attempt also failed — re-raise with helpful message
                raise RuntimeError(
                    f"Gemini quota exhausted for {model}.\n"
                    "Free-tier limits: 15 req/min, 1 500 req/day.\n"
                    "Options: (a) wait a minute and retry, "
                    "(b) enable billing on Google AI Studio, "
                    "(c) switch to --model gpt-4o-mini."
                ) from exc
            raise


def _call_anthropic(system: str, user: str, model: str) -> str:
    import anthropic  # type: ignore[import-untyped]

    client = anthropic.Anthropic()
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": user}],
    }
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    return resp.content[0].text  # type: ignore[attr-defined]


def _provider_for(slug: str) -> str:
    if slug in _API_MODELS:
        return _API_MODELS[slug]
    if slug.startswith(("gpt-", "o1", "o3")):
        return "openai"
    if slug.startswith("gemini"):
        return "gemini"
    if slug.startswith("claude"):
        return "anthropic"
    raise ValueError(f"Unknown model slug: {slug!r}. Use --model with a known slug.")


_CALLERS = {"openai": _call_openai, "gemini": _call_gemini, "anthropic": _call_anthropic}


def call_model(slug: str, system: str, user: str) -> str:
    """Call the appropriate API based on the model slug."""
    provider = _provider_for(slug)
    key = _ENV_KEYS.get(provider, "")
    if not os.environ.get(key):
        raise RuntimeError(f"{key} not set — cannot call model {slug!r}")
    return _CALLERS[provider](system, user, slug)


# ── Slug helpers ──────────────────────────────────────────────────────────────


def to_slug(name: str) -> str:
    """Sanitise a model name for use as a filename."""
    return name.replace("/", "-").replace(":", "-").replace(" ", "-").lower()


def slug_from_file(path: Path) -> str:
    return path.stem


# ── Generation step ───────────────────────────────────────────────────────────


_BIAS_SLUGS = [
    "anchoring",
    "framing",
    "loss_aversion",
    "confirmation_bias",
    "sunk_cost_fallacy",
]

# Suffix appended to the generation prompt when requesting a single bias type.
# Instructs the model to produce JSON for one bias only (fits within token limits).
_SINGLE_BIAS_SUFFIX = (
    "\n\n---\n"
    "IMPORTANT: Generate examples ONLY for the following bias type: **{bias_slug}**.\n"
    "Return a JSON object with keys `_metadata` and `{bias_slug}` only.\n"
    "Do NOT generate examples for other bias types."
)


def _gen_one_bias(model: str, slug: str, gen_prompt: str) -> dict[str, Any]:
    """Call the model for a single bias type; return parsed dict."""
    user = gen_prompt + _SINGLE_BIAS_SUFFIX.format(bias_slug=slug)
    raw = call_model(to_slug(model), system="", user=user)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON for bias '{slug}': {exc}\n---\n{raw[:500]}") from exc
    if slug not in parsed:
        raise ValueError(
            f"Bias key '{slug}' missing in response. Got keys: {list(parsed.keys())}"
        )
    return parsed


def cmd_gen(model: str, force: bool, single_call: bool) -> None:
    """Run generation: prompt_for_examples → model → json1.

    Default mode (--by-bias): runs one API call per bias type and merges the results.
    This avoids token-limit truncation that occurs when generating all 5 biases at once.
    Use --single-call to request all biases in one call (may truncate for large models).
    """
    slug = to_slug(model)
    out_file = _GEN_DIR / f"{slug}.json"
    _GEN_DIR.mkdir(parents=True, exist_ok=True)

    if out_file.exists() and not force:
        print(f"Already exists: {out_file}  (use --force to overwrite)")
        return

    if not _GEN_PROMPT_FILE.exists():
        print(f"Generation prompt not found: {_GEN_PROMPT_FILE}")
        sys.exit(1)

    gen_prompt = _GEN_PROMPT_FILE.read_text(encoding="utf-8")
    print(f"Generating with {model} ...")
    print(f"  Prompt: {_GEN_PROMPT_FILE.name}  ({len(gen_prompt)} chars)")
    print(f"  Output: {out_file}")

    if single_call:
        # Legacy single-call mode — may truncate for long outputs
        print("  Mode: single call (all biases at once — may truncate)")
        raw = call_model(slug, system="", user=gen_prompt)
        try:
            merged = json.loads(raw)
        except json.JSONDecodeError as exc:
            err_file = out_file.with_suffix(".error.txt")
            err_file.write_text(raw, encoding="utf-8")
            print(f"  ERROR: response is not valid JSON — saved raw to {err_file}")
            print(f"  JSON error: {exc}")
            sys.exit(1)
    else:
        # Default: one call per bias type, then merge
        print(f"  Mode: by-bias ({len(_BIAS_SLUGS)} separate calls — avoids token-limit truncation)")
        merged: dict[str, Any] = {}
        first_meta: dict[str, Any] = {}
        for i, bias_slug in enumerate(_BIAS_SLUGS, 1):
            print(f"  [{i}/{len(_BIAS_SLUGS)}] {bias_slug} ...", end=" ", flush=True)
            try:
                part = _gen_one_bias(model, bias_slug, gen_prompt)
                if not first_meta and "_metadata" in part:
                    first_meta = part["_metadata"]
                merged[bias_slug] = part[bias_slug]
                print(f"✅ {len(part[bias_slug])} examples")
            except (ValueError, RuntimeError) as exc:
                print(f"ERROR\n    {exc}")
                sys.exit(1)
        merged["_metadata"] = first_meta

    # Ensure _metadata.model is populated
    merged.setdefault("_metadata", {})
    merged["_metadata"].setdefault("model", model)

    out_file.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(v) for k, v in merged.items() if k != "_metadata" and isinstance(v, list))
    print(f"  ✅ Saved {total} examples total → {out_file}")


# ── Evaluation step ───────────────────────────────────────────────────────────


def cmd_eval(gen_model: str, eval_model: str, force: bool) -> None:
    """Run evaluation: prompt_for_evaluating + json1 → eval_model → json2."""
    gen_slug = to_slug(gen_model)
    eval_slug = to_slug(eval_model)
    gen_file = _GEN_DIR / f"{gen_slug}.json"
    out_file = _EVAL_DIR / f"{gen_slug}__by__{eval_slug}.json"
    _EVAL_DIR.mkdir(parents=True, exist_ok=True)

    if out_file.exists() and not force:
        print(f"Already exists: {out_file}  (use --force to overwrite)")
        return

    if not gen_file.exists():
        print(f"Generation file not found: {gen_file}")
        print(f"  Run: python pipeline.py gen --model {gen_model}")
        sys.exit(1)

    if not _EVAL_PROMPT_FILE.exists():
        print(f"Evaluation prompt not found: {_EVAL_PROMPT_FILE}")
        sys.exit(1)

    eval_prompt = _EVAL_PROMPT_FILE.read_text(encoding="utf-8")
    json1_text = gen_file.read_text(encoding="utf-8")
    json1_hash = hashlib.sha256(json1_text.encode()).hexdigest()

    # System = evaluation instructions; User = the json1 input
    user_msg = f"# Vstup\n\nZdrojový soubor: {gen_file.name}\nSHA256: {json1_hash}\n\n{json1_text}"

    print(f"Evaluating {gen_slug!r} with {eval_model} ...")
    print(f"  Input:  {gen_file.name}  ({len(json1_text)} chars)")
    print(f"  Output: {out_file}")
    print("  (this may take 1–3 minutes)")

    raw = call_model(eval_slug, system=eval_prompt, user=user_msg)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        err_file = out_file.with_suffix(".error.txt")
        err_file.write_text(raw, encoding="utf-8")
        print(f"  ERROR: response is not valid JSON — saved raw to {err_file}")
        print(f"  JSON error: {exc}")
        sys.exit(1)

    # Patch input_reference if model didn't fill source_file / sha256
    ref = parsed.setdefault("input_reference", {})
    ref.setdefault("source_file", str(gen_file))
    ref.setdefault("sha256", json1_hash)
    if not ref.get("generator_model"):
        gen_meta = json.loads(json1_text).get("_metadata", {})
        ref["generator_model"] = gen_meta.get("model", gen_model)

    out_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    score = parsed.get("statistics", {}).get("overall_mean_weighted", "?")
    print(f"  ✅ Saved  overall_mean_weighted={score} → {out_file}")


# ── HTML report ───────────────────────────────────────────────────────────────


def _score_color(score: float | None) -> str:
    if score is None:
        return "#e0e0e0"
    if score >= 80:
        return "#c8e6c9"   # green
    if score >= 65:
        return "#fff9c4"   # yellow
    if score >= 50:
        return "#ffe0b2"   # orange
    return "#ffcdd2"       # red


def _cell_html(json2: dict[str, Any], rel_path: str) -> str:
    stats = json2.get("statistics", {})
    score: float | None = stats.get("overall_mean_weighted")
    score_str = f"<b>{score:.1f}</b>" if score is not None else "<i>n/a</i>"

    # Count recommendations
    all_evals: list[dict[str, Any]] = []
    for examples in json2.get("evaluation_results", {}).values():
        all_evals.extend(examples)
    recs = [e.get("recommendation", "") for e in all_evals]
    n_total = len(recs)
    n_ok = recs.count("use_as_is")
    n_reject = recs.count("reject")

    summary = stats.get("overall_summary_feedback", "")
    summary_short = (summary[:120] + "…") if len(summary) > 120 else summary

    flagged_count = len(stats.get("flagged_examples", []))

    bg = _score_color(score)
    return (
        f'<td style="background:{bg};vertical-align:top;padding:6px;font-size:0.85em">'
        f"{score_str}<br>"
        f'<span title="use_as_is / total">✅ {n_ok}/{n_total}</span> '
        f'<span title="reject">❌ {n_reject}</span> '
        f'<span title="flagged">⚑ {flagged_count}</span><br>'
        f'<small style="color:#555">{summary_short}</small><br>'
        f'<a href="{rel_path}" target="_blank">json</a>'
        f"</td>"
    )


def cmd_report() -> None:
    """Scan gen/ and eval/ directories and produce report.html."""
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    gen_files = sorted(_GEN_DIR.glob("*.json")) if _GEN_DIR.exists() else []
    eval_files = sorted(_EVAL_DIR.glob("*__by__*.json")) if _EVAL_DIR.exists() else []

    if not gen_files and not eval_files:
        print("No data files found. Run gen and eval first.")
        return

    # Collect M1 and M2 slugs
    m1_slugs: list[str] = [slug_from_file(f) for f in gen_files]
    m2_slugs_set: set[str] = set()
    eval_index: dict[tuple[str, str], Path] = {}
    for f in eval_files:
        stem = slug_from_file(f)
        parts = stem.split("__by__", 1)
        if len(parts) == 2:
            m1, m2 = parts
            m2_slugs_set.add(m2)
            eval_index[(m1, m2)] = f

    # Also add M1s that appear only in eval/ (no gen/ file — e.g. manual)
    for m1, _ in eval_index:
        if m1 not in m1_slugs:
            m1_slugs.append(m1)

    m2_slugs = sorted(m2_slugs_set)
    m1_slugs = sorted(set(m1_slugs))

    # Load gen metadata
    gen_meta: dict[str, dict[str, Any]] = {}
    for f in gen_files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            gen_meta[slug_from_file(f)] = data.get("_metadata", {})
        except Exception:
            gen_meta[slug_from_file(f)] = {}

    # Build HTML
    rows_html = ""
    for m1 in m1_slugs:
        meta = gen_meta.get(m1, {})
        gen_at = meta.get("generated_at", "")
        gen_model_label = meta.get("model", m1)
        gen_file = _GEN_DIR / f"{m1}.json"
        gen_link = (
            f'<a href="gen/{m1}.json" target="_blank">json1</a>'
            if gen_file.exists()
            else '<span style="color:#aaa">no json1</span>'
        )
        row = (
            f'<tr><td style="font-weight:bold;background:#f5f5f5;padding:6px;'
            f'white-space:nowrap;font-size:0.85em">'
            f"{gen_model_label}<br>"
            f'<small style="color:#888">{gen_at[:10] if gen_at else "?"}</small><br>'
            f"{gen_link}</td>"
        )
        for m2 in m2_slugs:
            eval_file = eval_index.get((m1, m2))
            if eval_file and eval_file.exists():
                try:
                    data = json.loads(eval_file.read_text(encoding="utf-8"))
                    rel = f"eval/{eval_file.name}"
                    row += _cell_html(data, rel)
                except Exception as exc:
                    row += f'<td style="background:#fce4ec">parse error: {exc}</td>'
            else:
                row += '<td style="background:#fafafa;color:#bbb;text-align:center">—</td>'
        rows_html += row + "</tr>\n"

    header_cols = "".join(
        f'<th style="background:#e8eaf6;padding:6px;font-size:0.85em">{m2}</th>'
        for m2 in m2_slugs
    )

    html = f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<title>Example Evaluation Report</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 20px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; }}
  th {{ text-align: center; }}
  h1 {{ font-size: 1.4em; }}
  .legend span {{ display:inline-block; width:12px; height:12px; margin-right:4px; vertical-align:middle; }}
</style>
</head>
<body>
<h1>Cognitive Bias Example Evaluation</h1>
<p>
  <b>Rows = M1 (generator)</b> · <b>Columns = M2 (evaluator)</b><br>
  Cell: <b>weighted score</b> / ✅ use_as_is / ❌ reject / ⚑ flagged / <a>json2 link</a>
</p>
<p class="legend">
  Score legend:
  <span style="background:#c8e6c9"></span>≥80
  <span style="background:#fff9c4"></span>65–80
  <span style="background:#ffe0b2"></span>50–65
  <span style="background:#ffcdd2"></span>&lt;50
  <span style="background:#e0e0e0"></span>missing
</p>
<table>
<thead>
<tr>
  <th style="background:#e8eaf6;padding:6px">M1 \\ M2</th>
  {header_cols}
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
<hr>
<p style="font-size:0.8em;color:#888">
  Generated from: {_OUTPUT_DIR.relative_to(_PROJECT_ROOT)}<br>
  Regenerate: <code>python pipeline.py report</code>
</p>
</body>
</html>"""

    report_file = _OUTPUT_DIR / "report.html"
    report_file.write_text(html, encoding="utf-8")
    print(f"Report: {report_file}")
    print(f"  M1 models : {m1_slugs}")
    print(f"  M2 models : {m2_slugs}")
    print(f"  Cells filled: {len(eval_index)} / {len(m1_slugs) * len(m2_slugs)}")


# ── List commands ─────────────────────────────────────────────────────────────


def cmd_list() -> None:
    """List all gen and eval files found in the output directory."""
    print(f"\nOutput directory: {_OUTPUT_DIR}\n")

    print("── Generation files (json1) ─────────────────────────────")
    if _GEN_DIR.exists():
        for f in sorted(_GEN_DIR.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                meta = data.get("_metadata", {})
                total = sum(
                    len(v) for k, v in data.items()
                    if k != "_metadata" and isinstance(v, list)
                )
                print(f"  {f.name:45s}  {total} examples  model={meta.get('model', '?')}")
            except Exception as exc:
                print(f"  {f.name}  [ERROR: {exc}]")
    else:
        print("  (none)")

    print("\n── Evaluation files (json2) ─────────────────────────────")
    if _EVAL_DIR.exists():
        for f in sorted(_EVAL_DIR.glob("*__by__*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                score = data.get("statistics", {}).get("overall_mean_weighted", "?")
                eval_model = data.get("_metadata", {}).get("evaluator_model", "?")
                print(f"  {f.name:60s}  score={score}  evaluator={eval_model}")
            except Exception as exc:
                print(f"  {f.name}  [ERROR: {exc}]")
    else:
        print("  (none)")


def cmd_models() -> None:
    """Show which API models are available given the current API keys."""
    print("\nAPI model availability:\n")
    for slug, provider in sorted(_API_MODELS.items()):
        key = _ENV_KEYS.get(provider, "")
        ok = bool(os.environ.get(key))
        status = "✅ ready" if ok else f"⚠  missing {key}"
        print(f"  {slug:45s}  [{provider:9s}]  {status}")
    print("\nFor manual models, place files directly in:")
    print(f"  {_GEN_DIR}/<model-slug>.json")
    print(f"  {_EVAL_DIR}/<gen-slug>__by__<eval-slug>.json")


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("gen", help="Run generation step (P1 → M1 → json1)")
    p_gen.add_argument("--model", required=True, help="Generator model slug")
    p_gen.add_argument("--force", action="store_true", help="Overwrite existing output")
    p_gen.add_argument(
        "--single-call",
        action="store_true",
        default=False,
        help=(
            "Request all bias types in one API call instead of one-per-bias. "
            "May truncate for models with ≤16 384 token output limit."
        ),
    )

    p_eval = sub.add_parser("eval", help="Run evaluation step (P2 + json1 → M2 → json2)")
    p_eval.add_argument("--gen-model", required=True, help="Generator model slug (M1)")
    p_eval.add_argument("--eval-model", required=True, help="Evaluator model slug (M2)")
    p_eval.add_argument("--force", action="store_true", help="Overwrite existing output")

    sub.add_parser("report", help="Generate HTML report from all json2 files")
    sub.add_parser("list", help="List all existing gen/eval files")
    sub.add_parser("models", help="Show API model availability")

    args = parser.parse_args()

    if args.cmd == "gen":
        cmd_gen(args.model, args.force, single_call=args.single_call)
    elif args.cmd == "eval":
        cmd_eval(args.gen_model, args.eval_model, args.force)
    elif args.cmd == "report":
        cmd_report()
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "models":
        cmd_models()


if __name__ == "__main__":
    main()
