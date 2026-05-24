#!/usr/bin/env sh
set -eu

CONFIG_BASE="${XDG_CONFIG_HOME:-/var/lib/fullspektrum/flowstate/config}"
DATA_BASE="${XDG_DATA_HOME:-/var/lib/fullspektrum/flowstate/data}"
CONFIG_DIR="$CONFIG_BASE/flowstate"
DATA_DIR="$DATA_BASE/flowstate"
CONFIG_FILE="$CONFIG_DIR/config.yaml"

mkdir -p "$CONFIG_DIR/agents" "$CONFIG_DIR/skills" "$CONFIG_DIR/swarms" "$CONFIG_DIR/schemas" "$CONFIG_DIR/gates" "$DATA_DIR"

sync_dir() {
  src="$1"
  dest="$2"
  if [ -d "$src" ]; then
    mkdir -p "$dest"
    cp -R "$src/." "$dest/"
  fi
}

sync_dir /opt/fullspektrum/agents "$CONFIG_DIR/agents"
sync_dir /opt/fullspektrum/skills "$CONFIG_DIR/skills"
sync_dir /opt/fullspektrum/swarms "$CONFIG_DIR/swarms"
sync_dir /opt/fullspektrum/schemas "$CONFIG_DIR/schemas"

if [ -f "$CONFIG_FILE" ] && [ "${FULLSPEKTRUM_REWRITE_CONFIG:-false}" != "true" ]; then
  exit 0
fi

cat > "$CONFIG_FILE" <<CONFIG
providers:
  default: anthropic
  anthropic:
    model: "${ANTHROPIC_MODEL:-claude-sonnet-4-20250514}"
  ollama:
    host: "${OLLAMA_HOST:-http://ollama:11434}"
    model: llama3.2
qdrant:
  url: "${QDRANT_URL:-http://qdrant:6333}"
  collection: "${QDRANT_COLLECTION:-fullspektrum-npr}"
  api_key: "${QDRANT_API_KEY:-}"
embedding_model: "${EMBEDDING_MODEL:-nomic-embed-text}"
agent_dir: "$CONFIG_DIR/agents"
skill_dir: "$CONFIG_DIR/skills"
schema_dir: "$CONFIG_DIR/schemas"
gates_dir: "$CONFIG_DIR/gates"
data_dir: "$DATA_DIR"
default_agent: npr-onboarding
log_level: info
auth:
  enabled: ${FLOWSTATE_AUTH_ENABLED:-true}
  mode: "${FLOWSTATE_AUTH_MODE:-per-deployment-login}"
  secret: "${FLOWSTATE_AUTH_SECRET:-}"
  principal_id: "${FLOWSTATE_AUTH_PRINCIPAL_ID:-fullspektrum-demo}"
  display_name: "${FLOWSTATE_AUTH_DISPLAY_NAME:-FullSpektrum Demo}"
  secure_cookies: ${FLOWSTATE_AUTH_SECURE_COOKIES:-false}
  csrf_key: "${FLOWSTATE_AUTH_CSRF_KEY:-}"
  allowed_origins:
$(printf '%s' "${FLOWSTATE_AUTH_ALLOWED_ORIGINS:-localhost:*,127.0.0.1:*}" | tr ',' '\n' | sed 's/^/    - "/; s/$/"/')
CONFIG

