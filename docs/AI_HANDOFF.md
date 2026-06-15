# AI Handoff

Last reviewed: 2026-06-10

This file is the fastest way for another Codex instance or AI agent to continue the project without losing context.

## Project Objective

Build and maintain a high-signal AI coding product survey for TRAE SOLO / TRAE Work strategy. The project has four intertwined tracks:

1. market and product research on leading AI coding products;
2. technical mapping from papers and agent engineering patterns;
3. LPME, a product-manager benchmark for AI coding products;
4. daily / weekly update automation through GitHub and Feishu.

The final audience is not just engineers. The report should help a product owner reason about where AI coding products are going, what TRAE SOLO should learn, and how to evaluate product capability beyond model benchmarks.

## Non-Negotiable Product Belief

AI coding product capability is **model capability x product capability**.

Current models are not fully reliable, so product capability must compensate. When comparing products, always separate:

- model upper bound: model quality, model diversity, context length, reasoning effort, cost;
- product compensation: context engineering, task definition, workspace, permissions, verification, review, recovery, collaboration, deliverables, pricing and governance.

This belief should shape research, LPME scoring, daily PM notes, and TRAE SOLO implications.

## Current Core Product Pool

Use this order:

1. OpenAI Codex
2. Claude Code
3. Cursor
4. TRAE SOLO
5. GitHub Copilot
6. Windsurf / Devin Desktop
7. OpenClaw
8. Kimi Code
9. Zhipu GLM Coding Plan / CodeGeeX

Kimi Code and Zhipu / CodeGeeX are first-class products in the landscape and daily watch pool, but real-machine product testing currently focuses only on OpenAI Codex, Claude Code, Cursor, and TRAE SOLO.

OpenClaw remains in research and updates, but this local machine previously could not run it.

## Main Artifacts

- Baseline report: `research/market_research_base.md`
- Technical mapping: `research/technical_mapping.md`
- Technical deep dive: `research/technical_deep_dive.md`
- Paper notes: `research/paper_notes.md`
- Product breakthrough timeline: `research/product_breakthrough_timeline.md`
- LPME benchmark: `benchmark/README.md`
- LPME v0.2 protocol: `benchmark/lpme_v0.2/README.md`
- Product testing report: `research/product_testing_report_2026-06-04.md`
- Daily archive: `data/daily_updates/`
- Weekly archive: `data/weekly_updates/`
- Digest format contract: `automation/digest_format.md`
- Feishu subscription plan: `automation/feishu_subscription_plan.md`
- Operations runbook: `docs/OPERATIONS_RUNBOOK.md`

## Feishu / GitHub State

- GitHub remote: `git@github.com:GameScaler/ai_coding_project_survey.git`
- Feishu doc: `https://my.feishu.cn/docx/GVk4d22dSo3jEXxst72cRjMfntg`
- Feishu App Bot: `AI Coding Survey Bot`
- Fixed subscription group exists and is in `automation/feishu_subscribers.local.json` locally.
- App credentials are local-only. Do not commit or print secrets.

The current Feishu delivery architecture:

1. Codex automation tries to create a deep daily / weekly digest.
2. If no daily digest exists, launchd fallback generates a conservative daily digest.
3. `scripts/sync_delivery_runtime.sh` copies public digest files, sender scripts, subscribers, and local env into `~/.ai_coding_survey_delivery_runtime`.
4. `scripts/feishu_delivery_guard.py` sends unsent cards and records local state.
5. launchd watchdog runs the delivery guard every 10 minutes.

## Automation Snapshot

Codex automations:

- `ai-coding-daily-product-update`: daily 11:00, creates deep daily digest.
- `ai-coding-weekly-product-review`: Monday 11:20, creates weekly review for the last completed Monday-Sunday week.
- `ai-coding-feishu-delivery-guard`: daily guard calls `scripts/sync_and_run_feishu_delivery_guard.sh`.

macOS launchd jobs:

- `com.gamescaler.ai-coding-daily-fallback`: runs 11:15 and 11:45, creates conservative daily fallback if needed and sends.
- `com.gamescaler.ai-coding-weekly-fallback`: runs Monday 11:50 and 12:30, creates conservative weekly fallback if needed and sends.
- `com.gamescaler.ai-coding-feishu-delivery-guard`: runs every 10 minutes, sends pending daily / weekly cards.

The launchd runtime is outside Documents to avoid macOS privacy restrictions:

```text
~/.ai_coding_survey_delivery_runtime
```

## Daily Digest Requirements

Follow `automation/digest_format.md`.

Daily format:

- `Summary`
- `Product Updates`
- fixed product list in the exact order;
- `PM Notes`

If nothing meaningful happened, write:

```text
无新增产品级重大公开更新。
```

For each product with no update, write:

```text
- 无
```

Do not expose internal automation state. A DNS failure, crawler diff, or "source changed" event is not product news.

## Weekly Digest Requirements

Weekly reviews only cover completed Monday-Sunday weeks. Do not create in-progress weeks.

Weekly format:

- `Weekly Summary`
- `Head Product Signals`
- `Competitive Reading`
- `TRAE SOLO Implication`
- `LPME Implication`
- `Source Notes`

Weekly product signals must still include the full product pool. TRAE SOLO is the strategic interpretation target, not the only signal source.

## LPME Context

LPME means "Last Product Manager Examination". It evaluates whether an AI coding product can turn a real user goal into an acceptable outcome.

Current major dimensions:

- Interaction: task definition, workspace, state visibility, control.
- Model: upper bound, model diversity, cost / token efficiency, degradation strategy.
- Delivery: context, accuracy, workflow, verification, recovery.
- Scenario: personas, templates, plugins, cross-role usability.
- Commercialization / governance: pricing, plan limits, enterprise controls.

Real-machine evaluation currently covers OpenAI Codex, Claude Code, Cursor, and TRAE SOLO. Kimi Code and Zhipu / CodeGeeX are in research and update tracking, not scored in the current real-machine report.

## When Continuing Work

First run:

```bash
git status --short
```

Expect possible dirty files from automation. Do not revert them blindly.

If asked to update research:

1. read the relevant `research/*.md` file;
2. preserve the user's Feishu document structure and wording choices;
3. update GitHub first;
4. only then update Feishu if the task explicitly includes Feishu.

If asked to fix automation:

1. inspect Codex automation memory under `~/.codex/automations/`;
2. inspect launchd status;
3. inspect `~/.ai_coding_survey_delivery_runtime/data/feishu/`;
4. distinguish "digest not generated" from "digest generated but not sent".

## Common Failure Modes

- Codex daily automation does not run or fails before writing the daily file.
- Feishu DNS resolution fails in automation environment.
- `~/.ai_coding_survey_delivery_runtime` has permission drift; resync may fail.
- A digest was revised after being marked sent; use delivery guard `--force` only when intentionally resending.
- Public digest accidentally includes crawler or automation details; remove them.

## Safe Commands

Dry-run Feishu card:

```bash
python3 scripts/feishu_app_send.py data/daily_updates/YYYY-MM-DD.md \
  --title "AI Coding 产品更新｜YYYY-MM-DD" \
  --subscriber-file automation/feishu_subscribers.local.json \
  --subscription daily \
  --dry-run
```

Send pending cards:

```bash
scripts/sync_and_run_feishu_delivery_guard.sh
```

Generate fallback daily:

```bash
python3 scripts/generate_daily_fallback.py
```

Check launchd:

```bash
uid=$(id -u)
launchctl print "gui/$uid/com.gamescaler.ai-coding-daily-fallback"
launchctl print "gui/$uid/com.gamescaler.ai-coding-feishu-delivery-guard"
```
