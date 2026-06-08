#!/usr/bin/env bash
set -euo pipefail

missing=0

require_file() {
  if [[ ! -f "$1" ]]; then
    printf 'missing file: %s\n' "$1" >&2
    missing=1
  fi
}

require_dir() {
  if [[ ! -d "$1" ]]; then
    printf 'missing directory: %s\n' "$1" >&2
    missing=1
  fi
}

require_file docker-compose.yml
require_file .env.example
require_file scripts/write-flowstate-config.sh
require_file deploy/vps/flowstate.service
require_file deploy/vps/caddy.example.Caddyfile
require_file deploy/vps/nginx.example.conf
require_file deploy/vps/README.md
require_file deploy/vercel/README.md
require_file swarms/npr-onboarding.yml
require_dir agents
require_dir skills
require_dir schemas

if command -v docker >/dev/null 2>&1; then
  docker compose config >/dev/null
else
  printf 'warning: docker not found; skipped docker compose config validation\n' >&2
fi

if [[ -f .env ]]; then
  # shellcheck disable=SC1091
  set -a
  source .env
  set +a
  [[ -n "${ANTHROPIC_API_KEY:-}" ]] || printf 'warning: ANTHROPIC_API_KEY is empty\n' >&2
  [[ -n "${FLOWSTATE_AUTH_SECRET:-}" ]] || printf 'warning: FLOWSTATE_AUTH_SECRET is empty\n' >&2
  [[ -n "${FLOWSTATE_AUTH_CSRF_KEY:-}" ]] || printf 'warning: FLOWSTATE_AUTH_CSRF_KEY is empty\n' >&2
else
  printf 'warning: .env does not exist yet; copy .env.example to .env before running the demo\n' >&2
fi

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

printf 'demo scaffold looks coherent\n'
