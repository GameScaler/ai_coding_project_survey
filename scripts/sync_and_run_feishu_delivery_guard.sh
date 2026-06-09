#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
RUNTIME_DIR="$("$SCRIPT_DIR/sync_delivery_runtime.sh")"

exec "$RUNTIME_DIR/scripts/run_feishu_delivery_guard.sh"
