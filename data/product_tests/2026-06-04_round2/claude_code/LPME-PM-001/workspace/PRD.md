# PRD: PM Review Board

## Status
- Draft: initial product definition captured from brief, wireframe, and stakeholder feedback
- Ready for review: this document is ready for PM review once scope, assumptions, and edge cases below are accepted

## Overview
PM Review Board is a lightweight local review surface for product managers who receive AI-generated artifacts such as PRDs, landing pages, dashboards, and analysis memos. It gives PMs one place to see what is still a draft, what is ready for review, and what is blocked by unresolved risk.

The product should help a non-engineering PM understand artifact status, inspect the artifact preview without opening a modal, review visible risks, and leave or read reviewer comments before deciding whether to mark an item ready.

## Problem
PMs receive many AI-created artifacts in different formats. Today, it is hard to quickly answer:
- What is ready for my review?
- What still has unresolved risk?
- What acceptance checks should engineering use next?

Without a simple board, PMs may need to read raw output or code to understand readiness, which slows reviews and increases the chance of missing legal or delivery risks.

## Goals
- Show tasks grouped by status so PMs can quickly scan drafts, ready items, and blocked items.
- Keep the artifact preview visible on the main page.
- Make unresolved risks obvious before a PM marks anything ready.
- Show reviewer comments in plain language.
- Support an exportable acceptance checklist for engineering handoff.
- Work locally in a browser with a responsive layout for desktop and mobile.

## In Scope
- A task list grouped by status.
- Statuses for at least: Draft, Ready for Review, and Blocked.
- Artifact preview area displayed inline on the page.
- Risk checklist attached to the selected artifact.
- Reviewer comments attached to the selected artifact.
- A visible "Mark ready" action.
- A simple export summary interaction for review handoff.
- Responsive behavior for desktop and mobile layouts.
- Clear labels and explanations suitable for a non-engineering PM.

## Non-Goals
These are explicitly out of scope based on the brief:
- Real authentication or user accounts.
- Backend database or saved server-side state.
- External deployment.
- Real integrations with ticketing tools, messaging tools, or document platforms.
- Automatic artifact generation by an AI model.
- Code-level review workflows for engineers.

## Target User
### Primary user
- Product manager reviewing AI-generated artifacts.

### Secondary user
- Engineer receiving a clear acceptance checklist after PM review.

## Key User Stories
1. As a PM, I want to see tasks grouped by status so I can quickly identify what needs attention.
2. As a PM, I want to preview an artifact on the same page so I do not lose context.
3. As a PM, I want to see unresolved risks before marking anything ready.
4. As a PM, I want to read reviewer comments in plain language so I can decide what to do next.
5. As an engineer, I want acceptance checks to be exportable into a ticket so handoff is clearer.
6. As a legal reviewer, I want any artifact mentioning customer data to be visibly flagged.

## Core Experience
1. PM opens the board locally.
2. PM scans status groups to choose a task.
3. PM reads the visible artifact preview.
4. PM checks the risk checklist and comments.
5. PM decides whether the item stays draft, is blocked, or is marked ready for review.
6. PM exports the acceptance summary for handoff if needed.

## Functional Requirements
### Task list and status grouping
- The interface must show tasks grouped or filterable by status.
- The interface must include at least Draft and Ready for Review states, plus Blocked as shown in the wireframe.
- The PM must be able to switch between statuses and select an item.

### Artifact preview
- The selected artifact must appear inline in the main content area.
- The preview must not be hidden behind a modal.
- The preview should summarize the artifact in simple language.

### Risk checklist
- Each artifact must have a visible checklist of review risks.
- Unresolved risks must be easy to notice before the PM can confidently mark the item ready.
- If an artifact mentions customer data, that risk must be explicitly flagged.

### Reviewer comments
- The selected artifact must show reviewer comments on the main page.
- Comments should display role and priority so the PM can understand urgency.

### Mark ready action
- The product must include a visible action to mark an item ready.
- The UI should communicate when unresolved risks still remain.

### Export summary
- The product must provide a simple way to export or copy acceptance-oriented review details for engineering handoff.
- Because external integrations are out of scope, export should stay local to the prototype.

### Responsive behavior
- The prototype must support desktop and mobile layouts.
- On mobile, status navigation and selected task details must remain understandable in a vertical layout.

## Success Metrics
From the brief, success should be measured by:
- Time to first review under 3 minutes.
- PM can identify unresolved risk without reading code.
- Engineer receives clear acceptance checklist.

### Suggested prototype-level indicators
- A first-time viewer can identify draft vs ready items within 30 seconds.
- A first-time viewer can locate unresolved risk for the selected item within 15 seconds.
- A reviewer can understand the next handoff action without technical explanation.

## Assumptions
- This is a local-only prototype opened directly in a browser.
- Sample artifacts are enough to demonstrate the workflow.
- Export can be simulated locally and does not need file generation or third-party delivery.
- The PM prefers readability and plain language over dense product terminology.
- Risk visibility matters more than editing depth in this version.

## Edge Cases
- No tasks exist in a selected status.
- A task is marked ready and later needs to move back to draft.
- A blocked item has multiple unresolved risks.
- A legal-sensitive item mentions customer data and must remain visibly flagged.
- Reviewer comments conflict with one another.
- A PM views the board on a narrow mobile screen.
- An item appears mostly complete but still has one unresolved checklist item.
- Export is triggered for an item with open risks.

## Constraints
- Must work as a local HTML prototype without a build step.
- Must not claim backend behavior or integrations that do not exist.
- Must stay understandable to a non-engineering PM.

## Open Questions
- Should customer-data mentions always force Blocked status, or can they remain Draft with a prominent warning?
- What exact export format would best match engineering ticket workflows in a later version?
- Should future versions support artifact editing, or remain focused on review only?

## Ready for Review Checklist
This PRD is ready for review when the reviewer agrees that:
- Scope matches the provided brief.
- Non-goals exclude unsupported integrations and backend capabilities.
- Success metrics align with the feature brief.
- Legal and PM feedback are reflected in the risk workflow.
- User stories and edge cases are clear enough to drive acceptance tests.
