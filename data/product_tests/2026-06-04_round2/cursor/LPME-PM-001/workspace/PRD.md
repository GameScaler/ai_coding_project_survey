# PRD: PM Review Board

## Overview

A lightweight, local-first review board for product managers who receive AI-generated artifacts (PRDs, landing pages, dashboards, analysis memos). The board answers three questions in one place: what is ready for review, what is still in draft, and where unresolved risk remains.

## Problem

PMs accumulate many agent-produced artifacts with uneven quality. Without a single review surface, they lose time context-switching between files, miss risk signals buried in prose, and hand engineers incomplete acceptance context.

## Goals

| Goal | Description |
|------|-------------|
| Fast triage | PM reaches first meaningful review in under 3 minutes |
| Risk visibility | Unresolved risks are visible without reading source code |
| Clear handoff | Engineers receive an exportable acceptance checklist for tickets |

## In scope

1. **Task list grouped by status** — Draft, Ready for Review, Blocked (per wireframe).
2. **Artifact preview** — Inline preview panel (not a modal); supports representative artifact types from the brief.
3. **Risk checklist** — Standard items PMs must confirm before advancing a task.
4. **Reviewer comments** — Thread on each task; add comments while in draft.
5. **Mark ready** — Moves a draft task to Ready for Review only when all checklist items are checked.
6. **Export summary** — Board-level summary of tasks by status.
7. **Export acceptance checklist** — Per-task markdown suitable for pasting into a ticket.
8. **Customer-data flag** — Visual alert when artifact content mentions customer data (Legal feedback).

## Non-goals

- Real authentication or role-based access control
- Backend database or persistent server storage
- External deployment, CI, or third-party integrations (issue trackers, Slack, etc.)
- Live artifact ingestion from AI agents (prototype uses sample data)

## User stories

| ID | As a… | I want to… | So that… |
|----|--------|------------|----------|
| US-1 | PM | See tasks grouped by status | I know what needs attention first |
| US-2 | PM | Preview an artifact inline | I can judge quality without leaving the board |
| US-3 | PM | Complete a risk checklist before marking ready | I do not ship artifacts with open risks |
| US-4 | PM | Read and add reviewer comments | Context is captured on the task |
| US-5 | PM | Mark a draft task ready for review | The team knows it is queued for review |
| US-6 | Engineer | Export acceptance checks | I can paste them into a delivery ticket |
| US-7 | Legal | See when content mentions customer data | Privacy review is triggered early |

## Success metrics

| Metric | Target | Measurement (prototype) |
|--------|--------|-------------------------|
| Time to first review | &lt; 3 minutes | User opens board, selects task, sees preview + risks |
| Risk identification without code | PM spots open checklist items | Unresolved count shown on draft tasks |
| Engineer handoff clarity | Checklist export is complete | Export includes checks, summary, comments |

## UX requirements

### Desktop

- Left column: task list with status group headings.
- Right column: artifact preview, risk checklist, comments, actions.
- Header: title + Export Summary.

### Mobile

- Status filter tabs.
- Task selector dropdown.
- Stacked sections: preview → risks → comments (preview never hidden behind a modal).

## Functional requirements

### FR-1 Status grouping

Tasks appear under Draft, Ready for Review, or Blocked. Selecting a task loads its detail pane.

### FR-2 Risk gating

“Mark ready for review” is disabled until every risk checklist item is checked. A visible warning states how many risks remain.

### FR-3 Mark ready

When enabled, the action changes status from draft to ready for review and updates grouping.

### FR-4 Legal flag

If artifact preview text indicates customer data (prototype: `mentionsCustomerData` flag), show a prominent banner and PII badge on the task list.

### FR-5 Export

- **Board summary**: counts and titles by status.
- **Per-task checklist**: markdown with checkboxes, artifact summary, comments; copy to clipboard.

## Edge cases

| Case | Expected behavior |
|------|-------------------|
| Mark ready with open risks | Button disabled; warning shows unresolved count |
| Blocked task | Shown in Blocked group; risk checkboxes disabled; no Mark ready |
| Ready task | No Mark ready; risks read-only; comments read-only in prototype |
| All risks checked on draft | Enable Mark ready; show positive confirmation message |
| Artifact mentions customer data | Legal banner + PII badge; privacy checklist item highlighted in copy |
| Mobile filter excludes selected task | Auto-select first task in filtered list |
| Empty comments | Placeholder “No comments yet” |
| Clipboard unavailable | Copy button indicates manual copy fallback |

## Assumptions

- Review happens in a browser on a single machine; state resets on refresh (no persistence).
- “Blocked” is a manual or pre-set status in sample data; prototype does not auto-block.
- Risk checklist items are standardized for this product line; PMs do not customize items in v1.
- Customer-data detection in production would use content rules; prototype uses an explicit flag on sample tasks.
- Export format is markdown text for ticket paste, not API integration with Jira/Linear.

## Dependencies

- None external. Deliverable is static HTML/CSS/JS opened locally.

## Out of scope integrations (explicit)

No connections to: auth providers, databases, hosting, AI agent APIs, issue trackers, chat, or analytics pipelines.

## Rollout (conceptual)

1. Internal PM dogfood on static prototype.
2. Validate metrics via timed usability sessions.
3. If validated, spec persistence and agent webhook ingestion as a separate initiative.

## Open questions

- Who can move a task from Blocked back to Draft?
- Should Ready tasks allow reopening to Draft?
- Minimum checklist items for non-PRD artifact types (e.g. landing page only)?
