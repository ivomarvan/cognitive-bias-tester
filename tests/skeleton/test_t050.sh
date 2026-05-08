#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

die() {
  echo "test_t050: $*" >&2
  exit 1
}

[[ -f docker-compose.yml ]] && [[ -f frontend/package.json ]] && [[ -f frontend/Dockerfile ]] \
  || die "missing compose or frontend layout"

example_env="$(mktemp)"
trap 'rm -f "$example_env"' EXIT

awk '!/^[[:space:]]*#/ && NF' .env.example >"$example_env"
sed -i 's/^POSTGRES_PORT=.*/POSTGRES_PORT=15432/' "$example_env"
sed -i 's/^BACKEND_PORT=.*/BACKEND_PORT=18080/' "$example_env"
sed -i 's/^FRONTEND_PORT=.*/FRONTEND_PORT=15173/' "$example_env"

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cbt_t050_test}"

docker compose --env-file "$example_env" config >/dev/null \
  || die "docker compose config failed"

docker compose --env-file "$example_env" build frontend \
  || die "docker compose build frontend failed"

docker compose --env-file "$example_env" run --rm --no-deps frontend sh -c \
  "cd /app && npx vue-tsc --noEmit && npx eslint src/ && npm test && npm run build" \
  || die "frontend quality gate failed inside container"

if [[ "${SKIP_DOCKER_RUN:-}" == "1" ]]; then
  echo "test_t050: SKIP_DOCKER_RUN=1 — skipping compose up / health"
  echo "test_t050: OK"
  exit 0
fi

if ! docker info >/dev/null 2>&1; then
  die "Docker daemon not reachable — set SKIP_DOCKER_RUN=1 to skip runtime checks"
fi

compose_down() {
  docker compose --env-file "$example_env" down >/dev/null 2>&1 || true
}
trap 'compose_down; rm -f "$example_env"' EXIT

docker compose --env-file "$example_env" up -d frontend \
  || die "docker compose up frontend failed"

deadline=90
healthy=""
for ((i = 1; i <= deadline; i++)); do
  cid="$(docker compose --env-file "$example_env" ps -q frontend 2>/dev/null || true)"
  if [[ -n "$cid" ]]; then
    healthy="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$cid" 2>/dev/null || echo none)"
    if [[ "$healthy" == "healthy" ]]; then
      break
    fi
  fi
  sleep 1
done

[[ "$healthy" == "healthy" ]] || die "frontend not healthy within ${deadline}s (last: ${healthy:-unknown})"

compose_down
trap 'rm -f "$example_env"' EXIT

echo "test_t050: OK"
