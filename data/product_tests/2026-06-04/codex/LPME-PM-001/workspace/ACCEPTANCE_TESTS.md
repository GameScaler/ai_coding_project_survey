# PM Review Board Acceptance Tests

## Story 1: PM Views Tasks Grouped By Status

Acceptance tests:

- Given the PM opens `prototype/index.html`, when the page loads, then the task list shows Draft, Ready for Review, and Blocked groups.
- Given at least one draft task and one ready for review task exist, when the PM views the task list, then both statuses are visible without requiring an external service.
- Given the PM is on a mobile-sized screen, when the task list is shown, then status tabs are available and the page remains usable in a single-column layout.

## Story 2: PM Sees Unresolved Risk Before Marking Ready

Acceptance tests:

- Given a draft task has unresolved risks, when the task is selected, then the risk checklist shows each unresolved risk with its priority.
- Given a draft task has unresolved risks, when the PM views the primary action, then Mark ready is unavailable and explains that risks must be resolved first.
- Given all risks on a draft task are checked as resolved, when the PM views the primary action, then Mark ready becomes available.

## Story 3: PM Marks A Draft Artifact Ready

Acceptance tests:

- Given all risks on a draft task are resolved, when the PM clicks Mark ready, then the task status changes to Ready for Review.
- Given a task has moved to Ready for Review, when the task list rerenders, then the task appears under the Ready for Review group.
- Given a ready for review task is selected, when the PM views the status message, then it states that listed risks are cleared.

## Story 4: Reviewer Previews Artifact Without Modal

Acceptance tests:

- Given any task is selected, when the review workspace is shown, then the artifact preview is visible in the main page content.
- Given the PM reviews risks or comments, when they interact with the checklist or comment form, then the artifact preview remains visible and is not hidden behind a modal.
- Given the PM switches tasks, when the new task is selected, then the artifact preview updates to the selected task.

## Story 5: Reviewer Adds Comments

Acceptance tests:

- Given a selected task, when the PM enters a non-empty comment and submits it, then the comment appears in the Reviewer Comments section with the PM role.
- Given the comment field is empty, when the PM submits it, then no blank comment is added.
- Given the PM changes selected tasks, when comments render, then the comments match the selected artifact.

## Story 6: Engineer Gets Exportable Acceptance Checklist

Acceptance tests:

- Given any task is selected, when the PM clicks Export Summary or Export checklist, then a local export panel opens with ticket-ready text.
- Given the export panel is open, when the engineer reads the text, then it includes task title, status, owner, artifact type, unresolved risks, cleared risks, acceptance checks, and latest comments.
- Given the export panel is open, when Copy text is clicked, then the export text is copied when browser permissions allow it or selected for manual copying otherwise.
- Given export is used, then no external ticketing integration is invoked or implied.

## Story 7: Legal Reviewer Sees Customer-Data Flags

Acceptance tests:

- Given an artifact mentions customer data, when the task is selected, then a customer-data risk appears in the checklist.
- Given a customer-data risk is unresolved, when the PM tries to mark the artifact ready, then the action remains unavailable until the risk is cleared.
- Given the export summary is generated for an artifact with customer-data risk, then the risk appears in the unresolved or cleared risk section based on its checklist state.

## Story 8: Responsive Prototype Works Locally

Acceptance tests:

- Given the file is opened directly from disk, when the browser loads `prototype/index.html`, then the board renders without a local server.
- Given a desktop viewport, when the board is viewed, then the task list appears beside the artifact preview and review panel.
- Given a mobile viewport, when the board is viewed, then content stacks into a readable single-column flow with status tabs.
- Given text is long, when it appears in tasks, risks, comments, or metadata, then it wraps within its container without overlapping controls.
