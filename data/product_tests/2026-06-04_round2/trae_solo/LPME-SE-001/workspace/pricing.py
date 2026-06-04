from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    sku: str
    price: float
    quantity: int


def subtotal(items: list[CartItem]) -> float:
    return round(sum(item.price * item.quantity for item in items), 2)


def apply_discount(amount: float, discount_rate: float) -> float:
    """Apply a percentage discount to an amount."""
    # Safety: clamp discount_rate to prevent negative discounts (surcharges)
    # and over-discounting that would create negative subtotals.
    rate = min(max(discount_rate, 0.0), 1.0)
    return round(amount * (1 - rate), 2)


def shipping_fee(amount: float) -> float:
    if amount >= 100:
        return 0.0
    if amount >= 50:
        return 5.0
    return 9.0


def cart_total(items: list[CartItem], discount_rate: float = 0.0) -> float:
    base = subtotal(items)
    discounted = apply_discount(base, discount_rate)
    # Shipping should be charged based on the post-discount subtotal.
    shipping = shipping_fee(discounted)
    return round(discounted + shipping, 2)
