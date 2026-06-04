## Root cause
`apply_discount` accepted out-of-range discount values directly, which could increase totals for negative discounts or drive discounted subtotals below zero for discounts above 100%.

## Fix summary
Clamp `discount_rate` to the valid `[0.0, 1.0]` range before applying it, so discounts cannot increase the subtotal or make it negative. Existing total calculation continues to apply shipping from the post-discount subtotal.

## Verification
Command:
`python3 -m unittest discover -s tests -v`

Result:
- 3 tests ran
- All passed (`OK`)

## Risk notes
Low risk. The change is narrowly scoped to discount normalization and is covered by tests for negative discounts, discounts above 100%, and shipping based on discounted subtotal.
