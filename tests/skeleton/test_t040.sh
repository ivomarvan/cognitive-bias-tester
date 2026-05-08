#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

die() {
  echo "test_t040: $*" >&2
  exit 1
}

[[ -f docker-compose.yml ]] && [[ -f backend/pyproject.toml ]] \
  && [[ -f backend/alembic.ini ]] || die "missing compose or backend Alembic layout"

example_env="$(mktemp)"
trap 'rm -f "$example_env"' EXIT

awk '!/^[[:space:]]*#/ && NF' .env.example >"$example_env"
sed -i 's/^POSTGRES_PORT=.*/POSTGRES_PORT=15432/' "$example_env"
sed -i 's/^BACKEND_PORT=.*/BACKEND_PORT=18080/' "$example_env"

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cbt_t040_test}"

docker compose --env-file "$example_env" config >/dev/null \
  || die "docker compose config failed"

docker compose --env-file "$example_env" build backend \
  || die "docker compose build backend failed"

docker compose --env-file "$example_env" run --rm --no-deps backend sh -c \
  "cd /app && ruff check . && ruff format --check . && mypy src/ alembic/env.py --strict" \
  || die "quality gate failed inside backend container"

docker compose --env-file "$example_env" run --rm backend sh -c \
  "cd /app && pytest -m unit" \
  || die "unit tests failed inside backend container"

if [[ "${SKIP_DOCKER_RUN:-}" == "1" ]]; then
  echo "test_t040: SKIP_DOCKER_RUN=1 — skipping stack / alembic / integration"
  echo "test_t040: OK"
  exit 0
fi

if ! docker info >/dev/null 2>&1; then
  die "Docker daemon not reachable — set SKIP_DOCKER_RUN=1 to skip runtime checks"
fi

compose_down() {
  docker compose --env-file "$example_env" down -v >/dev/null 2>&1 || true
}
trap 'compose_down; rm -f "$example_env"' EXIT

docker compose --env-file "$example_env" up -d db backend \
  || die "docker compose up failed"

deadline=90
healthy=""
for ((i = 1; i <= deadline; i++)); do
  cid="$(docker compose --env-file "$example_env" ps -q backend 2>/dev/null || true)"
  if [[ -n "$cid" ]]; then
    healthy="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$cid" 2>/dev/null || echo none)"
    if [[ "$healthy" == "healthy" ]]; then
      break
    fi
  fi
  sleep 1
done

[[ "$healthy" == "healthy" ]] || die "backend not healthy within ${deadline}s (last: ${healthy:-unknown})"

docker compose --env-file "$example_env" exec -T backend alembic upgrade head \
  || die "alembic upgrade head failed"

docker compose --env-file "$example_env" exec -T backend pytest -q -m integration tests/test_db.py \
  || die "integration tests failed"

docker compose --env-file "$example_env" exec -T backend alembic downgrade base \
  || die "alembic downgrade base failed"

docker compose --env-file "$example_env" exec -T backend alembic upgrade head \
  || die "alembic upgrade head (second) failed"

compose_down
trap 'rm -f "$example_env"' EXIT

echo "test_t040: OK"
