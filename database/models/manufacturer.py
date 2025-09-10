from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    products = relationship("Product", back_populates="manufacturer")