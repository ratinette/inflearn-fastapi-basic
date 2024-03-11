from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
import datetime


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class Order(BaseModel):
    id: int
    created_at: datetime.datetime
    items: List[Item]


order = Order(
    id=123,
    created_at=datetime.datetime.now(),
    items=[Item(name="Widget", price=49.99), Item(name="Gizmo", price=29.99)]
)

json_compatible_order = jsonable_encoder(order)
print(json_compatible_order)