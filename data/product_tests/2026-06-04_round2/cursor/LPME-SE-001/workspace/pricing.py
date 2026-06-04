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
    return round(amount * (1 - discount_rate), 2)


def shipping_fee(amount: float) -> float:
    if amount >= 100:
        return 0.0
    if amount >= 50:
        return 5.0
    return 9.0


def cart_total(items: list[CartItem], discount_rate: float = 0.0) -> float:
    base = subtotal(items)
    discount_rate = max(0.0, min(1.0, discount_rate))
    discounted = apply_discount(base, discount_rate)
    shipping = shipping_fee(discounted)
    return round(discounted + shipping, 2)

