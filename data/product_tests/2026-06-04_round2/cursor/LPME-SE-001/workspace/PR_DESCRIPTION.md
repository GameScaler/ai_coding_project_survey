## Root cause

`cart_total` applied two ordering and validation mistakes:

1. **Shipping on pre-discount subtotal** — `shipping_fee` was called on the raw subtotal before the discount, so thresholds ($50 / $100) reflected the undiscounted amount.
2. **Unclamped `discount_rate`** — negative rates inflated the total (`1 - (-0.10) > 1`), and rates above `1.0` produced a negative discounted subtotal.

## Fix summary

In `cart_total` only:

- Clamp `discount_rate` to `[0.0, 1.0]`.
- Apply the discount first, then compute `shipping_fee` on the discounted subtotal.

Public API and helper names are unchanged.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

```
test_discount_above_one_is_capped_at_free_cart ... ok
test_negative_discount_is_treated_as_zero ... ok
test_shipping_uses_post_discount_subtotal ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

## Risk notes

- Low risk: single-function change, behavior aligned with existing tests.
- Callers that relied on pre-discount shipping tiers or out-of-range discount rates will see corrected totals; that is intentional per product rules.
