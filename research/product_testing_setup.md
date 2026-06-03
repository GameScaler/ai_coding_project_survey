# Product Testing Setup

更新时间：2026-06-03

## Local Installation Status

| Product | Local status | Version / path | Next required input |
| --- | --- | --- | --- |
| OpenAI Codex | Installed | `/Applications/Codex.app`, app version `26.601.21317`; CLI `/Applications/Codex.app/Contents/Resources/codex` | Already usable in this environment |
| Claude Code | Installed | CLI `/opt/homebrew/bin/claude`, version `2.1.161` | Anthropic login / API key |
| Cursor | Installed | `/Applications/Cursor.app`, CLI `/opt/homebrew/bin/cursor`, version `3.6.31` | Cursor account login and model/provider settings |
| TRAE SOLO | Installed | `/Applications/TRAE SOLO.app`, version `0.1.10` | TRAE account login; check auto-update to latest SOLO build on launch |
| Windsurf / Devin Desktop | Installed | `/Applications/Windsurf.app`, CLI `/opt/homebrew/bin/windsurf`, version `2.3.15` | Windsurf/Cognition login; Devin access if available |
| GitHub Copilot | Not separately installed | GitHub account is available in browser; Copilot availability not verified | Copilot subscription / app access if included in GameScaler account |

## Environment Notes

- Machine: macOS `26.2`, arm64.
- Node/npm installed through Homebrew for Claude Code CLI:
  - Node `v26.0.0`
  - npm `11.12.1`
- Cursor and Windsurf CLI `--version` commands printed macOS code-signing warnings but returned valid versions. This is common for Electron apps invoked from CLI and does not block installation.

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

## Credentials Needed From User

- Anthropic / Claude Code: login or API key.
- Cursor: account login and model/provider choice.
- TRAE SOLO: account login, and whether to use domestic or global account.
- Windsurf / Devin: account login and whether Devin access is enabled.
- GitHub Copilot: whether `GameScaler` has Copilot subscription and Copilot app access.

## Test Evidence Folder

Future test artifacts should be saved under:

- `data/product_tests/YYYY-MM-DD/product/task-id/`

Suggested files:

- `run_notes.md`
- `screenshots/`
- `output_artifacts/`
- `scorecard.yml`
- `raw_logs.txt`

