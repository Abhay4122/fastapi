from pydantic import BaseModel      # use to strict the requested data type
from datetime import datetime
from typing import Optional
# Schema for pydentic modal to verify the fields

class ProductBase(BaseModel):
    name: str
    price: int
    inventory: Optional[int] = 1


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True