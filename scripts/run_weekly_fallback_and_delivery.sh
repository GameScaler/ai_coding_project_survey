#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO_DIR="${SCRIPT_DIR:h}"
RUNTIME_DIR="${AI_CODING_DELIVERY_RUNTIME:-$HOME/.ai_coding_survey_delivery_runtime}"

cd "$REPO_DIR"
python3 scripts/generate_weekly_fallback.py

if [[ "$REPO_DIR" == "$RUNTIME_DIR" ]]; then
  exec scripts/run_feishu_delivery_guard.sh
fi

exec scripts/sync_and_run_feishu_delivery_guard.sh
