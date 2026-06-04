# Acceptance Tests: PM Review Board

Tests map to user stories in `PRD.md`. Run against `prototype/index.html` opened locally in a desktop browser; repeat critical paths at viewport ≤768px for mobile.

---

## US-1: Task list grouped by status

| ID | Given | When | Then |
|----|--------|------|------|
| AT-1.1 | Board loaded on desktop | User views left sidebar | Tasks appear under headings **Draft**, **Ready for Review**, and **Blocked** |
| AT-1.2 | Board loaded on mobile (≤768px) | User views status tabs | Tabs include All, Draft, Ready, Blocked |
| AT-1.3 | Mobile, Draft tab selected | User opens task dropdown | Only draft tasks are listed |
| AT-1.4 | Any task | User clicks a task in sidebar or mobile dropdown | That task becomes selected and detail pane updates |

---

## US-2: Inline artifact preview

| ID | Given | When | Then |
|----|--------|------|------|
| AT-2.1 | Task selected | User views main area | **Artifact preview** panel shows artifact type and body text inline |
| AT-2.2 | Any task | User looks for preview | Preview is not shown only inside a modal (always visible in main flow) |
| AT-2.3 | Mobile viewport | User scrolls detail | Preview appears above risk checklist and comments |

---

## US-3: Risk checklist before mark ready

| ID | Given | When | Then |
|----|--------|------|------|
| AT-3.1 | Draft task with unchecked risks (e.g. Checkout PRD v2) | User views risk section | Warning shows count of unresolved risks |
| AT-3.2 | Draft task with unchecked risks | User views **Mark ready for review** | Button is disabled |
| AT-3.3 | Draft task | User checks all risk items | Warning updates; button becomes enabled |
| AT-3.4 | Ready or Blocked task | User views risk checkboxes | Checkboxes are disabled (read-only) |

---

## US-4: Reviewer comments

| ID | Given | When | Then |
|----|--------|------|------|
| AT-4.1 | Task with existing comments (e.g. Usage dashboard spec) | User opens task | Prior comments show author and text |
| AT-4.2 | Draft task | User enters text and clicks **Add comment** | New comment appears in thread |
| AT-4.3 | Task with no comments | User opens task | Placeholder indicates no comments yet |
| AT-4.4 | Ready for review task | User views comments | Cannot add new comments (read-only in prototype) |

---

## US-5: Mark ready for review

| ID | Given | When | Then |
|----|--------|------|------|
| AT-5.1 | Draft task, all risks checked | User clicks **Mark ready for review** | Status pill shows **ready for review**; task moves to Ready for Review group |
| AT-5.2 | After AT-5.1 | User views actions | **Mark ready** control is no longer shown |
| AT-5.3 | Board includes draft and ready tasks | User scans sidebar | At least one **draft** and one **ready for review** task are visible without extra setup |

---

## US-6: Export acceptance checklist

| ID | Given | When | Then |
|----|--------|------|------|
| AT-6.1 | Any task selected | User clicks **Export acceptance checklist** | Modal shows markdown with title, status, checklist, summary, comments |
| AT-6.2 | Export modal open | User clicks **Copy to clipboard** | Content is copied (or user is prompted to copy manually) |
| AT-6.3 | Header | User clicks **Export Summary** | Modal shows board summary grouped by Draft / Ready / Blocked |

---

## US-7: Customer data flag

| ID | Given | When | Then |
|----|--------|------|------|
| AT-7.1 | Task mentioning customer data (e.g. Checkout PRD v2) | User views task list | **PII** badge appears on task |
| AT-7.2 | Same task | User views preview panel | Legal banner warns about customer data |
| AT-7.3 | Task without customer data (e.g. Onboarding landing page) | User views preview | Legal banner is not shown |

---

## Cross-cutting: Responsive & local

| ID | Given | When | Then |
|----|--------|------|------|
| AT-X.1 | `prototype/index.html` | User opens file via `file://` or local static server | Board renders with no network dependency |
| AT-X.2 | Desktop width (&gt;768px) | User resizes to mobile | Sidebar hides; tabs and task dropdown appear; content remains usable |
| AT-X.3 | Non-engineer PM | User completes AT-1.1 through AT-5.1 | Flow is understandable without reading source code |

---

## Non-goals verification

| ID | Given | When | Then |
|----|--------|------|------|
| AT-NG.1 | Prototype | User inspects UI and network | No login, no API calls to external services |
| AT-NG.2 | Prototype | User refreshes page | Task state resets to sample data (no database persistence) |

---

## Traceability matrix

| User story | Acceptance tests |
|------------|------------------|
| US-1 | AT-1.1 – AT-1.4 |
| US-2 | AT-2.1 – AT-2.3 |
| US-3 | AT-3.1 – AT-3.4 |
| US-4 | AT-4.1 – AT-4.4 |
| US-5 | AT-5.1 – AT-5.3 |
| US-6 | AT-6.1 – AT-6.3 |
| US-7 | AT-7.1 – AT-7.3 |
