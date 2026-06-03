from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)