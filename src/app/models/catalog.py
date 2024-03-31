from inspect import cleandoc

from sqlalchemy import Column, Integer, String, ForeignKey
from telegram import InlineKeyboardButton

from core.database import Base


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    count = Column(Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_text(self):
        return cleandoc(
            f"""
            *Позиция* - `{self.id}`;
            *Имя* - `{self.name}`;
            *Описание* - `{self.description}`;
            *Колиечство* - `{self.count}`.
            """
        )

    def to_button(self, offset: int, limit: int):
        return [
            InlineKeyboardButton(
                text=f"{self.name}; \n{self.description}",
                callback_data=f"catalog:{self.id}:{offset}:{limit}",
            )
        ]
