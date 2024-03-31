import time
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, BIGINT, Enum
from sqlalchemy.orm import relationship, Mapped

from core.database import Base

if TYPE_CHECKING:
    from .shopping_cart import ShoppingCart


class User(Base):
    __tablename__ = "user"
    
    tg_id = Column(BIGINT, primary_key=True)
    role = Column(Enum('user', 'admin', name="user_roles"), default="user", nullable=False)
    
    shopping_carts: Mapped[list["ShoppingCart"]] = relationship(
        back_populates="user", lazy="selectin"
    )
    
    def is_admin(self):
        return self.role == "admin"
