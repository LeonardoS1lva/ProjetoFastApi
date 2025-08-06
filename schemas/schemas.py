from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    status: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id_user: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    count: int
    flavor: str
    size: str
    unit_price: float

    class Config:
        from_attributes = True

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float
    items: List[OrderItemSchema]

    class Config:
        from_attributes = True