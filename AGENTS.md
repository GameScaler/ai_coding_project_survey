# Agent Instructions

This repository is an AI coding product survey and product-strategy workspace for TRAE SOLO / TRAE Work. Treat it as a living research system, not a generic notes repo.

## Start Here

Before making changes, read these files in order:

1. `README.md`
2. `docs/AI_HANDOFF.md`
3. `automation/digest_format.md`
4. `docs/OPERATIONS_RUNBOOK.md`

If the task touches LPME, also read:

1. `benchmark/README.md`
2. `benchmark/lpme_v0.2/README.md`
3. `research/product_testing_report_2026-06-04.md`

## Core Thesis

The guiding belief is:

> AI coding product capability = model capability x product capability.

Models define the upper bound, but current model capability is not reliable enough by itself. Product design must compensate through context engineering, workflow, verification, permissions, recovery, collaboration, cost controls, and deliverable management.

Do not evaluate products as model wrappers only. Always ask how the product turns imperfect model capability into a trustworthy user outcome.

## Core Product Pool

Use this fixed order everywhere:

1. OpenAI Codex
2. Claude Code
3. Cursor
4. TRAE SOLO
5. GitHub Copilot
6. Windsurf / Devin Desktop
7. OpenClaw
8. Kimi Code
9. Zhipu GLM Coding Plan / CodeGeeX

TRAE SOLO is the strategic interpretation target, not the only product to track. Every daily / weekly update must scan the whole pool.

## Public Digest Rules

`automation/digest_format.md` is the only source of truth for daily / weekly format.

Never put these into public GitHub digest, Feishu document, or bot card:

- crawler/source diff details;
- `Source / Changed / Excerpt` machine fields;
- internal automation errors;
- raw English changelog excerpts;
- secrets, tokens, API keys, chat invite links that should remain private.

If a product has no meaningful product-level update, write `无`. Do not force a PM interpretation from lightweight page changes.

Daily updates should be short and product-facing. Weekly reviews should synthesize product routes, model changes, product compensations for model gaps, TRAE SOLO implications, and LPME implications.

## Automation Commands

Generate source-gathering draft:

```bash
python3 scripts/daily_update.py --insecure-ssl
```

Generate conservative daily fallback only when no daily digest exists:

```bash
python3 scripts/generate_daily_fallback.py
```

Sync runtime and send pending Feishu cards:

```bash
scripts/sync_and_run_feishu_delivery_guard.sh
```

Run fallback generation plus delivery:

```bash
scripts/run_daily_fallback_and_delivery.sh
```

Check launchd jobs:

```bash
uid=$(id -u)
launchctl print "gui/$uid/com.gamescaler.ai-coding-daily-fallback"
launchctl print "gui/$uid/com.gamescaler.ai-coding-feishu-delivery-guard"
```

## Feishu Safety

Secrets live in ignored local files such as `.env.local` and `automation/feishu_subscribers.local.json`. Do not print, commit, or paste them into Feishu.

The Feishu push path is:

1. public digest markdown in `data/daily_updates/` or `data/weekly_updates/`;
2. runtime sync into `~/.ai_coding_survey_delivery_runtime`;
3. `scripts/feishu_delivery_guard.py` sends pending cards and records local state.

The launchd fallback only guarantees a conservative daily message exists and is sent. Deep PM judgment still belongs in the Codex daily automation or a human-reviewed update.

## Git Hygiene

The repo may have dirty files from automation, especially:

- `data/daily_updates/cache.json`
- same-day files in `data/daily_updates/`
- ignored Feishu delivery state/logs

Do not revert user or automation changes unless explicitly asked. Stage only the files relevant to the task. Before commit, run:

```bash
git diff --check
python3 -m py_compile scripts/*.py
```

For secret scanning staged changes:

```bash
git diff --cached | rg -n "sk-[A-Za-z0-9_-]{20,}|FEISHU_APP_SECRET=|ANTHROPIC_AUTH_TOKEN=|OPENAI_API_KEY=" || true
```
