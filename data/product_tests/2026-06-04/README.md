# LPME Product Test Run - 2026-06-04

## Scope

This is the first real-machine LPME v0.2 Core-3 run.

Products requested:

- OpenAI Codex
- Claude Code
- Cursor
- TRAE SOLO
- Kimi Code
- Zhipu GLM Coding Plan / CodeGeeX

OpenClaw is excluded because this machine cannot use it.

## What Actually Ran

Only **OpenAI Codex** completed all Core-3 tasks on this machine.

The other products were still tested for real local readiness, but Core-3 execution was blocked by login/model availability:

- Claude Code: installed, but CLI returned `Not logged in`.
- Cursor: `cursor agent` exists, but returned `Not logged in` and `No models available for this account`.
- TRAE SOLO: desktop UI opens and shows the MTC workspace, but task execution requires login.
- Kimi Code: CLI installed successfully, but prompt execution returned `No model configured`.
- CodeGeeX: Cursor extension `aminer.codegeex@2.21.3` installed successfully, but it is an IDE plugin rather than a headless agent and needs account/model setup.

## Score Summary

| Product | Current-machine status | Comparable LPME score? | Interaction | Model | Delivery | Scenario | Commercialization | Total |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI Codex | Core-3 completed | Yes | 16 | 15 | 29 | 12 | 8 | 80 |
| Claude Code | Not logged in | No | 8 | 0 | 0 | 4 | 3 | 15 |
| Cursor | Not logged in / no models | No | 9 | 0 | 0 | 5 | 3 | 17 |
| TRAE SOLO | UI reachable / not logged in | No | 12 | 0 | 0 | 8 | 4 | 24 |
| Kimi Code | Installed / no model configured | No | 8 | 0 | 0 | 5 | 4 | 17 |
| Zhipu GLM Coding Plan / CodeGeeX | Plugin installed / not runnable headless | No | 6 | 0 | 0 | 5 | 4 | 15 |

Important interpretation: blocked-product totals are **readiness scores on this machine**, not capability scores. They should not be used as final product ranking until accounts/models are configured.

## Codex Task Evidence

### LPME-SE-001

- Runtime: 61.8s
- Evidence: `codex/LPME-SE-001/raw_logs.txt`
- Verification: `python3 -m unittest discover -s tests -v` passed 3 tests.
- Output: fixed `pricing.py`, created `PR_DESCRIPTION.md`.
- PM read: very strong engineering delivery. It found the intended root cause, kept the patch minimal, and produced a useful PR note.

### LPME-PM-001

- Runtime: 263.9s
- Evidence: `codex/LPME-PM-001/raw_logs.txt`
- Output: `prototype/index.html`, `PRD.md`, `ACCEPTANCE_TESTS.md`.
- PM read: strong artifact generation and product thinking, including risk checklist, export text, comments, responsive CSS, and status transitions. Verification is mostly static because browser file access was blocked by local browser policy during my review.

### LPME-DS-001

- Runtime: 294.0s
- Evidence: `codex/LPME-DS-001/raw_logs.txt`
- Verification: `python3 analysis/acquisition_analysis.py` reran successfully.
- Output: cleaned CSV, channel summary, data quality report, four SVG charts, executive summary.
- PM read: strong data cleaning and caveat handling. It documented ambiguous channel mapping and missing spend assumptions, which is exactly the behavior LPME is designed to reward.

## Product-Level Reading

Codex shows strong **Delivery** because it can autonomously read files, edit, run commands, and create multi-file artifacts. Its weaker areas are **Interaction** and **Commercialization**: headless CLI is excellent for engineers, but it is not a product workbench for PM/data/ops users, and cost/model routing was not transparent enough. The three Codex runs consumed large token volumes: roughly 43k, 128k, and 96k tokens.

For TRAE SOLO, this run mainly exposes the next test requirement: account/model setup is mandatory before scoring. The visible MTC entry is product-directionally promising because it already presents task cards for web reading, research analysis, data mining, and file management. But LPME must score actual task completion, so it remains unscored as a full product until login is available.

For Claude Code, Cursor, Kimi Code, and CodeGeeX, the current blocker is not benchmark design but product access. The next run should configure each product account/model, then rerun the exact same Core-3 workspaces.

## TRAE SOLO Implications

- The strongest observed benchmark signal is not “Codex writes code well”; it is that product value comes from **agent harness + verification**. The model could be strong, but the product wins because it can read local files, edit, run tests, and leave evidence.
- TRAE SOLO should make model choice explicit: high-capability model for planning and complex edits, cheaper model for summarization/checklists, verifier model for risk review.
- Non-engineer tasks need artifact-level review, not diff-level review. Codex produced good artifacts, but its native surface is still engineer-centric.
- LPME should continue separating **model availability** from **product harness**. A product that cannot expose a model to the task is a product problem for the user, even if the underlying model might be strong.

