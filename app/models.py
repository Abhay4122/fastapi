from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database_config import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    # is_sale = Column(Boolean, server_default='true', nullable=False)
    inventory = Column(Integer, server_default='1')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))