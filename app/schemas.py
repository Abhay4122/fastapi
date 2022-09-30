from pydantic import BaseModel, EmailStr, Field, BaseSettings      # use to strict the requested data type
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# Schema for pydentic modal to verify the fields


class envSetting(BaseSettings):
    db_host: str
    db_user: str
    db_pass: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"

envs = envSetting()


class User(BaseModel):
    id: int
    email: EmailStr
    # password: str
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


class Test(BaseModel):
    issue_solve_date: datetime = Field(default_factory=datetime.now)

print(Test().issue_solve_date)


# Product


class ProductBase(BaseModel):
    name: str
    price: int
    inventory: Optional[int] = 1


class ProductCreate(ProductBase):
    name: str
    price: int
    user_id: int


class Product(ProductBase):
    id: int
    created_at: datetime
    user: User

    class Config:
        orm_mode = True

class ProdcutOut(BaseModel):
    Product: Product
    votes: int

    class Config:
        orm_mode = True
    


class Vote(BaseModel):
    product_id: int
    dir: conint(le=1)