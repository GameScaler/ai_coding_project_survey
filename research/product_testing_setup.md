# Product Testing Setup

更新时间：2026-06-04

## Local Installation Status

| Product | Local status | Version / path | Next required input |
| --- | --- | --- | --- |
| OpenAI Codex | Installed | `/Applications/Codex.app`, app version `26.601.21317`; CLI `/Applications/Codex.app/Contents/Resources/codex` | Already usable in this environment |
| Claude Code | Installed and round2 tested | CLI `/opt/homebrew/bin/claude`, version `2.1.161` | Completed Core-3 through local gateway; continue tracking permission/cost friction |
| Cursor | Installed and round2 tested | `/Applications/Cursor.app`, CLI `/opt/homebrew/bin/cursor`, version `3.6.31` observed earlier | Desktop logged in and completed Core-3; CLI auth/model state still needs separate setup |
| TRAE SOLO | Installed and round2 tested | `/Applications/TRAE SOLO.app`, version `0.1.10` observed earlier | Completed Core-3 through desktop; reliability/server-error retries need continued tracking |
| Windsurf / Devin Desktop | Installed | `/Applications/Windsurf.app`, CLI `/opt/homebrew/bin/windsurf`, version `2.3.15` | Windsurf/Cognition login; Devin access if available |
| Devin CLI | Installed | CLI `/opt/homebrew/bin/devin`, cask version `2026.5.26-3` | Cognition/Devin login |
| GitHub Copilot App | Installed | `/Applications/GitHub Copilot.app`, cask version `0.2.23` | GitHub login; Copilot subscription / technical preview access |
| OpenClaw | Deferred | 本机当前不可用/被禁用 | 进入主要产品池与公开信号监控；本轮不做真机实测 |
| Kimi Code | Installed, not in current LPME scored run | CLI `/Users/mvbj0638/.kimi-code/bin/kimi`, version `0.9.0` | Remains in market monitoring; do not include in product-testing score until the coding-agent task path is runnable |
| Zhipu GLM Coding Plan / CodeGeeX | Plugin installed, not in current LPME scored run | Cursor extension `aminer.codegeex@2.21.3` | Remains in market monitoring; do not include in product-testing score until the IDE/account task path is runnable |

## Environment Notes

- Machine: macOS `26.2`, arm64.
- Node/npm installed through Homebrew for Claude Code CLI:
  - Node `v26.0.0`
  - npm `11.12.1`
- Cursor and Windsurf CLI `--version` commands printed macOS code-signing warnings but returned valid versions. This is common for Electron apps invoked from CLI and does not block installation.
- Claude Code and Codex can be managed by `cc-switch`; do not write API keys into this repository. Configure keys only through local provider config, shell environment, or the product login flow.

## First Real-Use Test Plan

Do not start with all LPME tasks. First run a smoke test for each product:

1. Open the same repository: `ai_coding_project_survey`.
2. Ask the product to explain the LPME benchmark structure.
3. Ask it to make a tiny non-destructive edit in a scratch branch or temp file.
4. Ask it to run a local verification command.
5. Record:
   - onboarding friction;
   - context discovery quality;
   - plan quality;
   - approval / permission UX;
   - edit reliability;
   - verification behavior;
   - cost / model selection;
   - whether a non-engineer could understand the state.

After smoke tests, run LPME tasks in this order:

1. `LPME-SE-001`: unfamiliar repo bug fix.
2. `LPME-PM-001`: PRD to clickable prototype.
3. `LPME-DS-001`: acquisition cohort analysis.
4. `LPME-MKT-001`: campaign landing page.
5. `LPME-XFUNC-001`: multi-stakeholder handoff.

## First Real-Use Test Result - 2026-06-04

本轮已升级并运行 `benchmark/lpme_v0.2` Core-3。

- Codex completed all Core-3 tasks in round1 and is the strongest calibrated baseline.
- Cursor completed all Core-3 tasks in round2.
- Claude Code completed all Core-3 tasks in round2 after gateway configuration; permission/cost/correction friction was recorded.
- TRAE SOLO completed all Core-3 tasks in round2 after one retry each on PM and DS tasks.
- Kimi Code and CodeGeeX / GLM Coding Plan are excluded from the current scored product-testing section. They remain in market monitoring, not LPME scoring.
- Process files and scorecards: `data/product_tests/2026-06-04/` and `data/product_tests/2026-06-04_round2/`
- Full report: `research/product_testing_report_2026-06-04.md`

## Credential Handling

The user may provide API keys during setup, but keys must never be committed to git, pasted into Feishu, or stored in markdown.

Safe paths:

- `cc-switch provider add -a claude` or `cc-switch provider edit -a codex <provider-id>` for local provider config.
- Product-native login for Cursor, TRAE SOLO, Windsurf/Devin, and GitHub Copilot App.
- Shell environment variables for one-off test runs.

Current local observation:

- `cc-switch env tools` reports Claude and Codex installed.
- Codex already has a current provider configured locally.
- Claude Code is configured locally through `~/.claude/settings.json` and has completed the Core-3 run. Do not store the gateway token in this repository.

## Credentials Needed From User

- Claude Code: no immediate input for this run; next work is repeatability/cost tracking under the configured local gateway.
- Cursor: optional CLI agent login/model setup if we want reproducible headless runs beyond desktop.
- TRAE SOLO: no immediate login input needed; next work is repeatability/reliability tracking and paid-plan/model visibility if available.
- Windsurf / Devin: account login and whether Devin access is enabled.
- GitHub Copilot: whether `GameScaler` has Copilot subscription and Copilot app access.
- Devin: whether the account has Devin Desktop/cloud agent access.
- Kimi Code: only needed if we decide to bring it back into LPME scoring after a runnable coding-agent path is available.
- Zhipu / CodeGeeX: only needed if we decide to bring it back into LPME scoring after a runnable IDE/account path is available.

## Test Evidence Folder

Future test artifacts should be saved under:

- `data/product_tests/YYYY-MM-DD/product/task-id/`

Suggested files:

- `run_notes.md`
- `screenshots/`
- `output_artifacts/`
- `scorecard.yml`
- `raw_logs.txt`
