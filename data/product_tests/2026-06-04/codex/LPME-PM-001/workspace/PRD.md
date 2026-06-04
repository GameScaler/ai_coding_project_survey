# PM Review Board PRD

## Overview

Product managers receive many AI-generated artifacts, including PRDs, landing pages, dashboards, and analysis memos. The PM Review Board gives them one lightweight place to see what is still a draft, what is ready for review, and what has unresolved risk before work is handed to engineering or another reviewer.

## Problem

AI agents can produce useful project artifacts quickly, but PMs still need to inspect readiness, risks, and acceptance checks. Without a shared review surface, high-priority risks such as customer-data mentions or incomplete acceptance criteria can be missed, and engineers may receive unclear handoff instructions.

## Goals

- Help PMs start reviewing an AI-generated artifact in under 3 minutes.
- Make unresolved risks visible before an artifact can be marked ready.
- Keep the artifact preview visible while the PM reviews risks and comments.
- Produce a clear, paste-ready acceptance checklist for engineering handoff.
- Flag artifacts that mention customer data so they receive explicit review.

## Scope

- Task list grouped by status: draft, ready for review, and blocked.
- Artifact preview area that is visible in the main review workspace.
- Risk checklist with severity and completion state.
- Reviewer comments with role labels.
- Mark ready action for draft artifacts after unresolved risks are cleared.
- Local export summary containing status, unresolved risks, cleared risks, comments, and acceptance checks.
- Responsive desktop and mobile layouts matching the rough wireframe.

## Non-Goals

- No real authentication.
- No backend database or persistence across browser refreshes.
- No external deployment.
- No third-party ticketing, messaging, analytics, storage, or legal-system integrations.
- No AI artifact generation inside the board.
- No role-based permissions beyond showing reviewer role labels in comments.

## Primary Users

- Product manager: reviews AI-generated artifacts and decides when they are ready.
- Engineer: receives acceptance checks and risk context after PM review.
- Designer: reviews visible artifact content without opening a modal.
- Legal reviewer: expects customer-data mentions to be flagged before readiness.

## User Stories

1. As a PM, I want tasks grouped by status so I can quickly find drafts, review-ready work, and blocked items.
2. As a PM, I want unresolved risks visible before marking an artifact ready so I do not miss high-priority issues.
3. As a PM, I want to preview the artifact beside the review checklist so I can evaluate context without opening a modal.
4. As a reviewer, I want to leave comments with my role so later reviewers understand the decision history.
5. As an engineer, I want an exportable acceptance checklist so I can paste clear checks into a ticket.
6. As a legal reviewer, I want artifacts that mention customer data to be flagged so they are not accidentally marked ready.

## Functional Requirements

- The board shows task groups for draft, ready for review, and blocked.
- Selecting a task updates the preview, risk checklist, comments, and export text.
- Each risk has a label, priority, and resolved/unresolved state.
- Draft artifacts cannot be marked ready while any listed risk is unresolved.
- Marking a draft artifact ready moves it into the ready for review status group.
- Ready for review artifacts show that listed risks are cleared.
- Blocked artifacts show why they cannot be marked ready.
- The export summary is local text only and must not imply a live external integration.
- The prototype must work by opening `prototype/index.html` directly in a browser.

## Metrics

- Time to first review: median PM can select a task and identify the first unresolved risk in under 3 minutes.
- Risk visibility: PM can identify whether an artifact has unresolved risk without reading source code.
- Handoff clarity: engineer can identify acceptance checks and unresolved risks from exported ticket text.
- Review completion: percentage of draft artifacts moved to ready for review only after all risks are cleared.
- Customer-data safety: percentage of artifacts mentioning customer data that show a visible customer-data risk flag.

## Edge Cases

- A task has no risks: show a clear no-unresolved-risks state and allow Mark ready if it is a draft.
- A task has multiple high-priority risks: show all risks and prevent Mark ready until each is cleared.
- A ready for review task receives a new unresolved risk: status should be revisited and the task should no longer appear risk-free.
- A blocked task has cleared risks: the board should still communicate why it is blocked until the blocking reason is resolved.
- A comment is empty: do not add it to the comment list.
- Long task names, comments, and risk text: wrap text within the panel without hiding controls.
- Small screens: status filtering, selected task, preview, risks, and comments remain accessible in a single-column flow.
- Browser refresh in the prototype: state may reset because persistence is out of scope.

## Assumptions

- Initial task data can be embedded in the local prototype.
- Status values are limited to draft, ready for review, and blocked for this version.
- The PM is responsible for clearing risk checklist items before marking an artifact ready.
- Export means generating local, copyable text for a ticket, not sending data to an external tool.
- Customer-data detection is represented as an explicit checklist flag in this prototype, not automated scanning.
- Comments are reviewer notes for context and are not threaded discussions.

## Open Questions

- Should a ready for review artifact automatically move back to draft if a new risk is added later?
- What minimum acceptance-check template should be required for each artifact type?
- Should blocked have a separate required owner field in a future version?
