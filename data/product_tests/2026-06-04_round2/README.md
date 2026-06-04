# LPME Product Test Run - 2026-06-04 Round 2

## Scope

This round focuses on products the user had installed and logged in locally:

- Cursor
- TRAE SOLO
- Kimi Code

OpenClaw is excluded on this machine. Claude Code is installed but not logged in yet, so it is handled after this round.

## What Actually Ran

Cursor and TRAE SOLO both completed LPME v0.2 Core-3:

1. `LPME-SE-001`: unfamiliar Python repo bug fix.
2. `LPME-PM-001`: PRD to clickable prototype.
3. `LPME-DS-001`: messy acquisition cohort analysis.

Kimi Code was checked through both desktop and CLI surfaces, but the coding-agent path was blocked by account/model entitlement:

- Kimi desktop chat was logged in and usable as a general chat surface.
- Kimi Work page stayed at workspace preparation.
- Kimi Code CLI `0.9.0` returned `No providers configured`.
- Login flow failed with a membership entitlement verification message.

This means Kimi is recorded as an access/commercialization blocker, not as a failed model-capability run.

## Score Summary

| Product | Current-machine status | Comparable LPME score? | Interaction | Model | Delivery | Scenario | Commercialization | Total |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cursor | Core-3 completed | Yes | 18 | 16 | 29 | 14 | 8 | 85 |
| TRAE SOLO | Core-3 completed after retries | Yes | 16 | 13 | 27 | 15 | 8 | 79 |
| Kimi Code | Blocked by provider/model entitlement | No | 10 | 2 | 0 | 5 | 3 | 20 |

Important interpretation: Cursor and TRAE SOLO are comparable LPME Core-3 scores in this round. Kimi Code is a current-machine access score only.

## Product-Level Reading

Cursor is the strongest full-run product in this round. The key strength is not only code generation quality; it is the combination of workspace, file editing, command execution, and artifact creation. The main gap is that the desktop run was usable while the CLI path was not logged in and exposed no model list, which hurts reproducibility and automation.

TRAE SOLO completed all three tasks and is directionally the closest to a non-engineer workbench. Its MTC surface fits PM/data/ops workflows better than a pure IDE. The important weakness is reliability: PM and DS tasks both hit a server error on the first attempt and needed one retry. That is exactly the kind of product-layer issue that prevents model capability from becoming dependable user value.

Kimi Code cannot be treated as a completed LPME run. The underlying Kimi model may be capable, but the coding-agent product path did not expose a runnable provider/model under this account. For a product benchmark, this still matters: if the user cannot connect the model to the workflow, the product capability is effectively unavailable.

## TRAE SOLO Implications

- The benchmark should continue to score product harness and model access separately. Kimi is the clean example: model brand strength does not matter if the agent surface cannot start.
- TRAE SOLO should treat reliability as a first-order product metric. A retry that eventually succeeds is still a serious PM-side trust cost.
- Cursor shows why a product workbench needs artifact generation plus verification. It is not enough to answer; the product must leave files, tests, and reviewable handoff material.
- TRAE SOLO's opportunity is to combine Cursor-like execution with a clearer non-engineer workspace: task status, artifact preview, risk review, verification evidence, and business-language approvals.

## Evidence

- Cursor task outputs: `cursor/LPME-*/workspace`
- TRAE SOLO task outputs: `trae_solo/LPME-*/workspace`
- Kimi access notes: `kimi_code/LPME-*/run_notes.md`
- Machine-readable scorecards: `scorecards.yml`
