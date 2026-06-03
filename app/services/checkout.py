from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


def create_order_from_cart(
    db: Session,
    customer_name: str,
    phone_number: str,
    payment_method: str,
    cart: dict[str, int],
    user_id: int | None = None,
) -> Order:
    new_order = Order(
        customer_name=customer_name,
        phone_number=phone_number,
        payment_method=payment_method,
        status="Pending",
        user_id=user_id,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product_id, quantity in cart.items():
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=int(product_id),
            quantity=quantity,
        )
        db.add(order_item)

    db.commit()
    return new_order