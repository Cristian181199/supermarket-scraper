from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    products = relationship("Product", back_populates="store")