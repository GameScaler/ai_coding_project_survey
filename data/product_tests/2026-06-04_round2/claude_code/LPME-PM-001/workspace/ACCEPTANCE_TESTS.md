# Acceptance Tests: PM Review Board

## Status
- Draft: acceptance coverage created from the feature brief, wireframe, and feedback
- Ready for review: this file is ready once the PM confirms the user stories and expected outcomes match the intended workflow

## Test Format
Each section maps to a user story. These tests are written for a non-engineering PM and describe what should be true when using the local prototype.

---

## User Story 1
**As a PM, I want to see tasks grouped by status so I can quickly identify what needs attention.**

### Acceptance Criteria
- The interface shows status views for Draft, Ready for Review, and Blocked.
- Selecting a status updates the visible task list.
- The number of items in each status is understandable at a glance.

### Test Cases
1. Open `prototype/index.html` in a desktop browser.
   - Expected: The page loads without a server.
   - Expected: The left-side task area clearly shows status options.
2. Click **Draft**.
   - Expected: Only draft items are shown in the task list.
3. Click **Ready for Review**.
   - Expected: Only ready items are shown in the task list.
4. Click **Blocked**.
   - Expected: Only blocked items are shown in the task list.
5. Repeat steps 2 to 4 on a mobile-sized viewport.
   - Expected: The status controls remain usable and readable.

---

## User Story 2
**As a PM, I want to preview an artifact on the same page so I do not lose context.**

### Acceptance Criteria
- A selected task updates the artifact preview area.
- The preview appears inline on the page.
- The preview is not hidden behind a modal.

### Test Cases
1. In any status view, click a task in the list.
   - Expected: The artifact preview updates immediately.
2. Review the layout on desktop.
   - Expected: The preview is visible beside or near the task list without opening another screen.
3. Review the layout on mobile.
   - Expected: The preview remains visible in the page flow after task selection.
4. Confirm no modal or pop-up is required to see core preview content.
   - Expected: The preview is always accessible from the main page.

---

## User Story 3
**As a PM, I want to see unresolved risks before marking anything ready.**

### Acceptance Criteria
- The selected task shows a risk checklist.
- Unresolved risk is visible in the summary area.
- A blocked item clearly explains why it is blocked.
- Draft and ready states are both represented in the prototype.

### Test Cases
1. Select the draft PRD task.
   - Expected: The screen shows a checklist with at least one unresolved item.
   - Expected: The review summary explains that risk review is still needed.
2. Select the blocked memo task.
   - Expected: The summary clearly says the item is blocked by unresolved risk.
   - Expected: The customer-data concern is visibly called out.
3. Check all risk boxes for a non-blocked draft item.
   - Expected: The summary updates to show the item is ready for review.
4. Click **Mark ready** after all visible risks are resolved for a draft item.
   - Expected: The item moves into the Ready for Review state.

---

## User Story 4
**As a PM, I want to read reviewer comments in plain language so I can decide what to do next.**

### Acceptance Criteria
- Reviewer comments appear for the selected artifact.
- Each comment shows who made it.
- Priority is understandable without technical knowledge.

### Test Cases
1. Select each sample task one by one.
   - Expected: Each task displays reviewer comments relevant to that item.
2. Review the comments section.
   - Expected: Each comment includes a role label such as PM, Designer, Engineer, or Legal.
   - Expected: Each comment includes a visible priority label.
3. Read the comment text.
   - Expected: The comment language is understandable to a non-engineering PM.

---

## User Story 5
**As an engineer, I want acceptance checks to be exportable into a ticket so handoff is clearer.**

### Acceptance Criteria
- The prototype includes a visible export action.
- The exported content summarizes the selected artifact state, acceptance checks, and open risks.
- The export behavior stays local and does not depend on an external integration.

### Test Cases
1. Select any task.
2. Click **Export Summary**.
   - Expected: A local export-style interaction appears.
   - Expected: The exported summary includes artifact name, current state, acceptance checks, and open risks.
3. Confirm the page does not claim to send data to any external tool.
   - Expected: Export remains local to the prototype.

---

## User Story 6
**As a legal reviewer, I want any artifact mentioning customer data to be visibly flagged.**

### Acceptance Criteria
- At least one sample artifact demonstrates the customer-data risk case.
- The flag is visible in the risk checklist and review summary.
- The PM can understand that additional review is needed.

### Test Cases
1. Select the blocked analysis memo.
   - Expected: The risk checklist includes a customer-data flag.
   - Expected: The review summary explains that legal-sensitive content is still flagged.
2. Review the comments section for the same task.
   - Expected: A Legal comment explains the concern in plain language.
3. Attempt to treat the blocked item as ready.
   - Expected: The interface continues to communicate that the item is blocked until the issue is addressed.

---

## Cross-Device Acceptance Tests
1. Open the prototype in a desktop-sized viewport.
   - Expected: The task list and detail area are easy to scan side by side.
2. Open the prototype in a mobile-sized viewport.
   - Expected: The layout stacks vertically without losing status, preview, risk, or comment visibility.
3. Interact with status filters, task selection, and export on both desktop and mobile.
   - Expected: Core flows remain usable in both layouts.

---

## Ready for Review Checklist
This acceptance test set is ready for review when:
- Every key user story from the PRD is covered.
- Tests reflect the brief and stakeholder feedback.
- Draft and ready-for-review states are explicitly tested.
- Legal-sensitive customer-data handling is included.
- No test expects unsupported backend or external integrations.
