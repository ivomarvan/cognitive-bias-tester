#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

die() {
  echo "test_t060: $*" >&2
  exit 1
}

[[ -f docker-compose.yml ]] && [[ -f .env.example ]] || die "missing compose or .env.example"

example_env="$(mktemp)"
trap 'rm -f "$example_env"' EXIT

# Non-comment, non-empty lines from template (same pattern as other skeleton tests).
awk '!/^[[:space:]]*#/ && NF' .env.example >"$example_env"
sed -i 's/^POSTGRES_PORT=.*/POSTGRES_PORT=15432/' "$example_env"
sed -i 's/^BACKEND_PORT=.*/BACKEND_PORT=18080/' "$example_env"
sed -i 's/^FRONTEND_PORT=.*/FRONTEND_PORT=15173/' "$example_env"

read_port() {
  local key="$1"
  local line val
  line="$(grep -E "^${key}=" "$example_env" | head -1)" || die "missing ${key} in env file"
  val="${line#${key}=}"
  val="${val%$'\r'}"
  printf '%s' "$val"
}

BACKEND_HOST_PORT="$(read_port BACKEND_PORT)"
FRONTEND_HOST_PORT="$(read_port FRONTEND_PORT)"

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cbt_t060_test}"

docker compose --env-file "$example_env" config >/dev/null \
  || die "docker compose config failed"

compose_down() {
  docker compose --env-file "$example_env" down -v >/dev/null 2>&1 || true
}

wait_healthy() {
  local service="$1"
  local deadline="$2"
  local healthy=""
  local cid=""
  for ((i = 1; i <= deadline; i++)); do
    cid="$(docker compose --env-file "$example_env" ps -q "$service" 2>/dev/null || true)"
    if [[ -n "$cid" ]]; then
      healthy="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$cid" 2>/dev/null || echo none)"
      if [[ "$healthy" == "healthy" ]]; then
        return 0
      fi
    fi
    sleep 1
  done
  die "${service} not healthy within ${deadline}s (last: ${healthy:-unknown}, cid: ${cid:-none})"
}

run_smoke() {
  compose_down
  trap 'compose_down; rm -f "$example_env"' EXIT

  if ! docker info >/dev/null 2>&1; then
    die "Docker daemon not reachable"
  fi

  docker compose --env-file "$example_env" up -d \
    || die "docker compose up -d failed"

  wait_healthy db 30
  wait_healthy backend 90
  wait_healthy frontend 90

  local health_json
  health_json="$(curl -fsS "http://127.0.0.1:${BACKEND_HOST_PORT}/v1/health")" \
    || die "backend health curl failed (port ${BACKEND_HOST_PORT})"
  grep -q '"status"' <<<"$health_json" || die "backend health JSON missing status"
  grep -q '"ok"' <<<"$health_json" || die "backend health JSON missing ok"

  local html
  html="$(curl -fsS "http://127.0.0.1:${FRONTEND_HOST_PORT}/")" \
    || die "frontend curl failed (port ${FRONTEND_HOST_PORT})"
  grep -qi '<!doctype html' <<<"$html" || grep -qi '<html' <<<"$html" || die "frontend root does not look like HTML"

  compose_down
  trap 'rm -f "$example_env"' EXIT
}

run_smoke
run_smoke

echo "test_t060: OK"
