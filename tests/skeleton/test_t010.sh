#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

die() {
  echo "test_t010: $*" >&2
  exit 1
}

require_path() {
  local rel="$1"
  [[ -e "$ROOT/$rel" ]] || die "missing path: $rel"
}

require_file() {
  local rel="$1"
  [[ -f "$ROOT/$rel" ]] || die "missing file: $rel"
}

require_dir() {
  local rel="$1"
  [[ -d "$ROOT/$rel" ]] || die "missing directory: $rel"
}

# Happy path — required tree and files
require_dir "backend"
if [[ ! -f "$ROOT/backend/.gitkeep" && ! -f "$ROOT/backend/pyproject.toml" ]]; then
  die "missing backend scaffold (expected .gitkeep from T010 or pyproject.toml from T030+)"
fi
require_file "frontend/.gitkeep"
require_dir "doc/architecture/decisions"
require_file "doc/guides/.gitkeep"
require_file "doc/external/.gitkeep"
require_file "nogit_data/.gitkeep"
require_file "experiments/.gitkeep"
require_file ".gitignore"
require_file "README.md"
require_file "doc/architecture/decisions/ADR-001-use-postgresql.md"
require_file "doc/architecture/decisions/ADR-002-ethics-framework.md"
require_file "tests/skeleton/test_t010.sh"

# README keywords (placeholder completeness)
for token in \
  "MVP" \
  "docker compose" \
  "doc/project-progress/spec.md" \
  "doc/project-progress/roadmap.md" \
  "GNU General Public License" \
  "Quick start" \
  "backend/" \
  "frontend/"
do
  grep -Fq "$token" README.md || die "README.md missing keyword or phrase: $token"
done

# Edge case 1 — .gitignore literals (exact line match)
IGNORE="$ROOT/.gitignore"
for line in \
  __pycache__ \
  node_modules \
  .env \
  nogit_data/ \
  dist/ \
  .mypy_cache \
  .ruff_cache
do
  grep -Fxq "$line" "$IGNORE" || die ".gitignore missing required line: $line"
done

# Edge case 2 — ADR structure
for adr in \
  "doc/architecture/decisions/ADR-001-use-postgresql.md" \
  "doc/architecture/decisions/ADR-002-ethics-framework.md"
do
  for heading in "## Context" "## Decision" "## Consequences"; do
    grep -Fq "$heading" "$ROOT/$adr" || die "$adr missing section: $heading"
  done
  grep -Fq "**Status**: Accepted" "$ROOT/$adr" || die "$adr missing accepted status line"
done

echo "test_t010: OK"
