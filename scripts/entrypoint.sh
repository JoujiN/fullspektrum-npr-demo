#!/usr/bin/env sh
set -eu

export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/var/lib/fullspektrum/flowstate/config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-/var/lib/fullspektrum/flowstate/data}"

write-flowstate-config

flowstate memory-tools install || true

exec flowstate serve --host "${FLOWSTATE_HOST:-0.0.0.0}" --port "${PORT:-8080}"

