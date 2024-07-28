from inspect import cleandoc

from sqlalchemy import CheckConstraint, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from telegram import InlineKeyboardButton

from core.database import Base


class Purchase(Base):
    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True)
    
    tg_id = Column(BigInteger, ForeignKey("user.tg_id", ondelete="CASCADE"))
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Integer, CheckConstraint('price >= 1', name='check_price'), nullable=False)
    count = Column(Integer, CheckConstraint('count >= 0', name='check_count'), default=1, nullable=False)
    file_unique_tg_id = Column(String, default=None, nullable=True)
    value = Column(String, nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_text(self):
        return cleandoc(
            f"""
            *Позиция* - `{self.id}`;
            *Имя* - `{self.name}`;
            *Описание* - `{self.description}`;
            *Количество* - `{self.count}`;
            *Выданный товар* - `{self.value}`.
            """
        )

    def to_button(self, offset: int, limit: int):
        return [
            InlineKeyboardButton(
                text=f"{self.name}; \n{self.description}",
                callback_data=f"purchase:{self.id}:{offset}:{limit}",
            )
        ]
