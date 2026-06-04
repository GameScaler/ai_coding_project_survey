# LPME Product Test Run - 2026-06-04 Round 2

## Scope

This is the calibrated Core-3 product test run for the four products with runnable task evidence:

- OpenAI Codex, evidence from `data/product_tests/2026-06-04/codex`
- Claude Code, evidence from `data/product_tests/2026-06-04_round2/claude_code`
- Cursor, evidence from `data/product_tests/2026-06-04_round2/cursor`
- TRAE SOLO, evidence from `data/product_tests/2026-06-04_round2/trae_solo`

Products that were not runnable through the same coding-agent task path are excluded from this scored product-testing section. They remain in market and daily/weekly monitoring, but not in the LPME score table.

## Score Summary

| Product | Status | Interaction | Model | Delivery | Scenario | Commercialization | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI Codex | Core-3 completed | 17 | 17 | 30 | 14 | 10 | 88 |
| Cursor | Core-3 completed | 18 | 16 | 29 | 14 | 8 | 85 |
| Claude Code | Core-3 completed after permission/correction friction | 15 | 16 | 27 | 13 | 11 | 82 |
| TRAE SOLO | Core-3 completed after product retries | 16 | 13 | 27 | 15 | 9 | 80 |

The spread is intentionally not huge: all four products can now complete Core-3. The ranking reflects product reliability and the cost of turning model capability into verified outcome.

## Product-Level Reading

**Codex is the strongest baseline** because it completed Core-3 with the least product ceremony: read files, edited code, ran commands, generated artifacts, and left verification evidence. It is still engineer-centric, but its execution harness is the cleanest.

**Cursor is the best workbench-style competitor** in this run. Its desktop agent produced strong PM and DS artifacts, and the product surface feels closer to a durable IDE workbench. Its gap is reproducibility: desktop worked, while CLI/model state was less transparent.

**Claude Code is powerful but expensive/frictionful in this environment.** It completed the tasks after we configured the internal gateway. The outputs were strong, but default permission mode caused Bash friction, DS needed one correction loop for mixed-date parsing, and token/cost usage was high.

**TRAE SOLO is directionally closest to the non-engineer workbench.** It completed Core-3 and has the right MTC product instinct, but PM and DS tasks each needed a retry after server errors. Reliability and model transparency are the key gaps.

## TRAE SOLO Implications

- Learn from Codex's execution harness: local context, file edits, command execution, tests, and evidence.
- Learn from Cursor's workbench: tasks, artifacts, status, preview, and review loops.
- Learn from Claude Code's transparency, but avoid pushing non-engineers into terminal-level permission and cost friction.
- Preserve TRAE SOLO's scenario advantage, but make retry/recovery, task state, model routing, and verification evidence first-class.

## Evidence Links

- Codex round1 evidence: `../2026-06-04/codex`
- Claude Code round2 evidence: `claude_code`
- Cursor round2 evidence: `cursor`
- TRAE SOLO round2 evidence: `trae_solo`
- Machine-readable scorecard: `scorecards.yml`
