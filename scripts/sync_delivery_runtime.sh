#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO_DIR="${SCRIPT_DIR:h}"
RUNTIME_DIR="${AI_CODING_DELIVERY_RUNTIME:-$HOME/.ai_coding_survey_delivery_runtime}"

mkdir -p \
  "$RUNTIME_DIR/scripts" \
  "$RUNTIME_DIR/automation" \
  "$RUNTIME_DIR/data/daily_updates" \
  "$RUNTIME_DIR/data/weekly_updates" \
  "$RUNTIME_DIR/data/feishu"

rsync -a "$REPO_DIR/scripts/feishu_app_send.py" "$RUNTIME_DIR/scripts/"
rsync -a "$REPO_DIR/scripts/feishu_delivery_guard.py" "$RUNTIME_DIR/scripts/"
rsync -a "$REPO_DIR/scripts/generate_daily_fallback.py" "$RUNTIME_DIR/scripts/"
rsync -a "$REPO_DIR/scripts/generate_weekly_fallback.py" "$RUNTIME_DIR/scripts/"
rsync -a "$REPO_DIR/scripts/run_feishu_delivery_guard.sh" "$RUNTIME_DIR/scripts/"
rsync -a "$REPO_DIR/scripts/run_daily_fallback_and_delivery.sh" "$RUNTIME_DIR/scripts/"
rsync -a "$REPO_DIR/scripts/run_weekly_fallback_and_delivery.sh" "$RUNTIME_DIR/scripts/"
chmod +x "$RUNTIME_DIR/scripts/"*.py "$RUNTIME_DIR/scripts/"*.sh

rsync -a "$REPO_DIR/automation/feishu_subscribers.local.json" "$RUNTIME_DIR/automation/"

if [[ -f "$REPO_DIR/.env.local" ]]; then
  rsync -a "$REPO_DIR/.env.local" "$RUNTIME_DIR/.env.local"
fi

rsync -a --include='*/' --include='*.md' --exclude='*' \
  "$REPO_DIR/data/daily_updates/" "$RUNTIME_DIR/data/daily_updates/"
rsync -a --include='*/' --include='*.md' --exclude='*' \
  "$REPO_DIR/data/weekly_updates/" "$RUNTIME_DIR/data/weekly_updates/"

if [[ ! -f "$RUNTIME_DIR/data/feishu/delivery_state.local.json" \
      && -f "$REPO_DIR/data/feishu/delivery_state.local.json" ]]; then
  rsync -a "$REPO_DIR/data/feishu/delivery_state.local.json" "$RUNTIME_DIR/data/feishu/"
fi

echo "$RUNTIME_DIR"
