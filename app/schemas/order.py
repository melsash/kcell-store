from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_name: str
    phone_number: str
    product_id: int
    quantity: int = 1


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str

    class Config:
        from_attributes = True