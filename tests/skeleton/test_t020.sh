#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

die() {
  echo "test_t020: $*" >&2
  exit 1
}

[[ -f docker-compose.yml ]] && [[ -f .env.example ]] || die "missing docker-compose.yml or .env.example"

if grep -qE '^[[:space:]]*version[[:space:]]*:' docker-compose.yml; then
  die "docker-compose.yml must not contain a top-level version: field"
fi

example_env="$(mktemp)"
no_pw_env="$(mktemp)"

rm_temp() {
  rm -f "$example_env" "$no_pw_env"
}
trap rm_temp EXIT

awk '!/^[[:space:]]*#/ && NF' .env.example >"$example_env"
# Use a non-default host port so the test does not require a free 5432 on the machine.
sed -i 's/^POSTGRES_PORT=.*/POSTGRES_PORT=15432/' "$example_env"
awk '!/^POSTGRES_PASSWORD=/' "$example_env" >"$no_pw_env"

docker compose --env-file "$example_env" config >/dev/null \
  || die "docker compose config failed with .env.example values"

if docker compose --env-file "$no_pw_env" config >/dev/null 2>&1; then
  die "expected docker compose config to fail when POSTGRES_PASSWORD is unset"
fi

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cbt_t020_test}"

compose_down() {
  docker compose --env-file "$example_env" down -v >/dev/null 2>&1 || true
}

if [[ "${SKIP_DOCKER_RUN:-}" == "1" ]]; then
  echo "test_t020: SKIP_DOCKER_RUN=1 — skipping compose up / health wait"
  echo "test_t020: OK"
  exit 0
fi

if ! docker info >/dev/null 2>&1; then
  die "Docker daemon not reachable — start Docker or set SKIP_DOCKER_RUN=1 for partial check"
fi

trap 'compose_down; rm_temp' EXIT

docker compose --env-file "$example_env" up -d db \
  || die "docker compose up -d db failed"

for ((i = 1; i <= 30; i++)); do
  cid="$(docker compose --env-file "$example_env" ps -q db 2>/dev/null || true)"
  if [[ -n "$cid" ]]; then
    health="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$cid" 2>/dev/null || echo none)"
    if [[ "$health" == "healthy" ]]; then
      echo "test_t020: db is healthy"
      compose_down
      trap rm_temp EXIT
      echo "test_t020: OK"
      exit 0
    fi
  fi
  sleep 1
done

docker compose --env-file "$example_env" ps || true
die "db did not become healthy within 30s"
