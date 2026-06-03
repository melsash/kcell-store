from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    new_order = Order(
        customer_name=order.customer_name,
        phone_number=order.phone_number,
        payment_method=getattr(order, "payment_method", "Kaspi"),
        status="Pending"
)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_item = OrderItem(
        order_id=new_order.id,
        product_id=order.product_id,
        quantity=order.quantity
    )

    db.add(order_item)
    db.commit()

    return {
        "message": "Order created successfully",
        "order_id": new_order.id
    }