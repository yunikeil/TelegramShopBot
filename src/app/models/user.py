from inspect import cleandoc
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, Integer, BigInteger, Enum
from sqlalchemy.orm import relationship, Mapped

from core.database import Base

if TYPE_CHECKING:
    from .shopping_cart import ShoppingCart
    from .purchase import Purchase


class User(Base):
    __tablename__ = "user"
    
    tg_id = Column(BigInteger, primary_key=True)
    role = Column(Enum('user', 'admin', name="user_roles"), default="user", nullable=False)
    balance = Column(Integer, CheckConstraint('balance >= 0', name='check_balance'), default=0, nullable=False)
    
    shopping_carts: Mapped[list["ShoppingCart"]] = relationship(
        back_populates="user", lazy="selectin"
    )
    purchases: Mapped[list["Purchase"]] = relationship(lazy="selectin")
    
    def get_amount_purhases(self):
        result = 0
        for purhase in self.purchases:
            result += purhase.count * purhase.price
        
        return result
    
    def to_text(self):
        return cleandoc(
            f"""
            *id* - `{self.tg_id}`;
            *role* - `{self.role}`;
            *balance* - `{self.balance / 100}`;
            *ammount_purchases* - `{self.get_amount_purhases() / 100}`;
            *len_carts* - `{len(self.shopping_carts)}`;
            *len_purhases* - `{len(self.purchases)}`;
            """
        )
    
    def is_admin(self):
        return self.role == "admin"

