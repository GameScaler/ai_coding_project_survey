# LPME-SE-001: Unfamiliar Repo Bug Fix

You are evaluating an AI coding product.

Open this small Python repo, diagnose the failing behavior, implement the smallest safe fix, run tests, and prepare a PR description.

## Requirements

1. Do not rewrite the whole module.
2. Preserve existing public function names.
3. Run `python3 -m unittest discover -s tests -v`.
4. Write a short `PR_DESCRIPTION.md` with:
   - root cause;
   - fix summary;
   - verification command and result;
   - risk notes.

## Acceptance Criteria

- All tests pass.
- The fix handles negative discounts safely.
- Shipping should be charged on the post-discount subtotal.
- No broad unrelated refactor.
