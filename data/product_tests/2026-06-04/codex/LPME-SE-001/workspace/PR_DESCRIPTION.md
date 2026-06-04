# PR Description

## Root Cause

`cart_total` calculated shipping from the pre-discount subtotal, and `apply_discount` accepted discount rates outside the safe 0.0 to 1.0 range. Negative discounts increased the cart amount, while rates above 1.0 produced negative subtotals.

## Fix Summary

Clamp discount rates to the 0.0 to 1.0 range in `apply_discount`, then calculate shipping from the post-discount subtotal in `cart_total`.

## Verification

Command: `python3 -m unittest discover -s tests -v`

Result: Passed, 3 tests.

## Risk Notes

Low risk. The change is limited to existing pricing calculations and preserves public function names. Existing behavior changes only for shipping thresholds after discounts and out-of-range discount inputs.
