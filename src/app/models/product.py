from inspect import cleandoc

from sqlalchemy import CheckConstraint, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from telegram import InlineKeyboardButton

from core.database import Base


class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True)
    catalog_id = Column(Integer, ForeignKey("catalog.id", ondelete="CASCADE"), nullable=False)
    value = Column(String, nullable=False)
