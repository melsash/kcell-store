from app.database.db import Base, engine

from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem


def init_db():
    Base.metadata.create_all(bind=engine)