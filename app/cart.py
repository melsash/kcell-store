from __future__ import annotations

from fastapi import Request
from sqlalchemy.orm import Session

from app.models.product import Product

CART_SESSION_KEY = "cart"


def get_cart(request: Request) -> dict[str, int]:
    cart = request.session.get(CART_SESSION_KEY, {})
    if not isinstance(cart, dict):
        return {}
    return {str(k): int(v) for k, v in cart.items() if int(v) > 0}


def save_cart(request: Request, cart: dict[str, int]) -> None:
    request.session[CART_SESSION_KEY] = cart


def cart_item_count(request: Request) -> int:
    return sum(get_cart(request).values())


def add_to_cart(request: Request, product_id: int, quantity: int = 1) -> None:
    cart = get_cart(request)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    save_cart(request, cart)


def increase_quantity(request: Request, product_id: int) -> None:
    add_to_cart(request, product_id, 1)


def decrease_quantity(request: Request, product_id: int) -> None:
    cart = get_cart(request)
    key = str(product_id)
    if key not in cart:
        return
    cart[key] -= 1
    if cart[key] <= 0:
        del cart[key]
    save_cart(request, cart)


def remove_from_cart(request: Request, product_id: int) -> None:
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)


def clear_cart(request: Request) -> None:
    request.session[CART_SESSION_KEY] = {}


def build_cart_lines(request: Request, db: Session) -> tuple[list[dict], float]:
    cart = get_cart(request)
    lines: list[dict] = []
    total = 0.0

    for product_id, quantity in cart.items():
        product = db.query(Product).filter(Product.id == int(product_id)).first()
        if not product:
            continue
        subtotal = product.price * quantity
        total += subtotal
        lines.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return lines, total
