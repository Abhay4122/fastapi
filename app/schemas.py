from pydantic import BaseModel, EmailStr      # use to strict the requested data type
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


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: Optional[datetime] = datetime.today()
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_email: Optional[str] = None