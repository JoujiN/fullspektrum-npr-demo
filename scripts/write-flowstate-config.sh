#!/usr/bin/env sh
set -eu
umask 077

CONFIG_BASE="${XDG_CONFIG_HOME:-/var/lib/fullspektrum/flowstate/config}"
DATA_BASE="${XDG_DATA_HOME:-/var/lib/fullspektrum/flowstate/data}"
ASSET_ROOT="${FULLSPEKTRUM_ASSET_ROOT:-/opt/fullspektrum/npr-demo}"
CONFIG_DIR="$CONFIG_BASE/flowstate"
DATA_DIR="$DATA_BASE/flowstate"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
CONFIG_TMP="$CONFIG_FILE.tmp"

trap 'rm -f "$CONFIG_TMP"' EXIT

mkdir -p "$CONFIG_DIR/agents" "$CONFIG_DIR/skills" "$CONFIG_DIR/swarms" "$CONFIG_DIR/schemas" "$CONFIG_DIR/gates" "$DATA_DIR"

sync_dir() {
  src="$1"
  dest="$2"
  case "$dest" in
    "$CONFIG_DIR"/*) ;;
    *)
      printf 'refusing to sync outside config dir: %s\n' "$dest" >&2
      exit 1
      ;;
  esac

  rm -rf "$dest"
  mkdir -p "$dest"
  if [ -d "$src" ]; then
    cp -R "$src/." "$dest/"
  fi
}

sync_dir "$ASSET_ROOT/agents" "$CONFIG_DIR/agents"
sync_dir "$ASSET_ROOT/skills" "$CONFIG_DIR/skills"
sync_dir "$ASSET_ROOT/swarms" "$CONFIG_DIR/swarms"
sync_dir "$ASSET_ROOT/schemas" "$CONFIG_DIR/schemas"
sync_dir "$ASSET_ROOT/gates" "$CONFIG_DIR/gates"

rm -f "$CONFIG_TMP"
cat > "$CONFIG_TMP" <<CONFIG
providers:
  default: zai
  anthropic:
    api_key: "${ZAI_API_KEY}"
    host: ""
    model: "${ZAI_MODEL:-glm-4.6}"
    oauth:
        client_id: ""
        enabled: false
        scopes: ""
        token_file: ""
        use_oath: false
    plan: coding
CONFIG
# cat > "$CONFIG_TMP" <<CONFIG
# providers:
#   default: anthropic
#   anthropic:
#     model: "${ANTHROPIC_MODEL:-claude-sonnet-4-20250514}"
# CONFIG

if [ -n "${OLLAMA_HOST:-}" ]; then
  cat >> "$CONFIG_TMP" <<CONFIG
  ollama:
    host: "${OLLAMA_HOST}"
    model: "${OLLAMA_MODEL:-llama3.2}"
CONFIG
fi

if [ -n "${QDRANT_URL:-}" ]; then
  cat >> "$CONFIG_TMP" <<CONFIG
qdrant:
  url: "${QDRANT_URL}"
  collection: "${QDRANT_COLLECTION:-fullspektrum-npr}"
  api_key: "${QDRANT_API_KEY:-}"
CONFIG
fi

if [ -n "${EMBEDDING_MODEL:-}" ]; then
  cat >> "$CONFIG_TMP" <<CONFIG
embedding_model: "${EMBEDDING_MODEL}"
CONFIG
fi

cat >> "$CONFIG_TMP" <<CONFIG
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
  secure_cookies: ${FLOWSTATE_AUTH_SECURE_COOKIES:-true}
  csrf_key: "${FLOWSTATE_AUTH_CSRF_KEY:-}"
  allowed_origins:
$(printf '%s' "${FLOWSTATE_AUTH_ALLOWED_ORIGINS:-localhost:*,127.0.0.1:*}" | tr ',' '\n' | sed 's/^/    - "/; s/$/"/')
CONFIG

mv "$CONFIG_TMP" "$CONFIG_FILE"
chmod 0600 "$CONFIG_FILE"
