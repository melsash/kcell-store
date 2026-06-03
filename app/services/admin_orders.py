from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


def get_order_total(db: Session, order_id: int) -> float:
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    total = 0.0
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            total += product.price * item.quantity
    return total


def build_order_rows(db: Session) -> list[dict]:
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    rows = []
    for order in orders:
        rows.append(
            {
                "order": order,
                "total": get_order_total(db, order.id),
                "customer_email": "—",
            }
        )
    return rows
