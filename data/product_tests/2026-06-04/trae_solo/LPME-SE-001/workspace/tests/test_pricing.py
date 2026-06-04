import unittest

from pricing import CartItem, cart_total


class PricingTests(unittest.TestCase):
    def test_shipping_uses_post_discount_subtotal(self):
        items = [CartItem("pro-plan", 60.0, 2)]
        self.assertEqual(cart_total(items, discount_rate=0.25), 95.0)

    def test_negative_discount_is_treated_as_zero(self):
        items = [CartItem("starter", 20.0, 2)]
        self.assertEqual(cart_total(items, discount_rate=-0.10), 49.0)

    def test_discount_above_one_is_capped_at_free_cart(self):
        items = [CartItem("enterprise", 120.0, 1)]
        self.assertEqual(cart_total(items, discount_rate=1.5), 9.0)


if __name__ == "__main__":
    unittest.main()
