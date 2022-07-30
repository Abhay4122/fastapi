from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .orm_test import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_sale = Column(Boolen, default=True)
    inventory = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow())