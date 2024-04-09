from inspect import cleandoc

from sqlalchemy import CheckConstraint, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from telegram import InlineKeyboardButton

from core.database import Base
from .product import Product


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Integer, CheckConstraint('price >= 1', name='check_price'), nullable=False)
    file_unique_tg_id = Column(String, default=None, nullable=True)

    products: Mapped[list["Product"]] = relationship(lazy="selectin")
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_text(self):
        return cleandoc(
            f"""
            *Позиция* - `{self.id}`;
            *Имя* - `{self.name}`;
            *Описание* - `{self.description}`;
            *Цена* - `{self.price}`;
            *Колиечство* - `{len(self.products)}`;
            """
        )

    def to_button(self, offset: int, limit: int):
        return [
            InlineKeyboardButton(
                text=f"{self.name}; \n{self.description}",
                callback_data=f"catalog:{self.id}:{offset}:{limit}",
            )
        ]
