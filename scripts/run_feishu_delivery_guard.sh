#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO_DIR="${SCRIPT_DIR:h}"

cd "$REPO_DIR"
exec python3 scripts/feishu_delivery_guard.py \
  --daily-lookback-days 7 \
  --weekly-lookback-weeks 3 \
  --attempts 4 \
  --backoff-seconds 20
