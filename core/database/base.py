from time import time

from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    created_at = Column(Integer, default=int(time()), nullable=False)
    updated_at = Column(Integer, default=int(time()), onupdate=int(time()), nullable=False)

    def to_dict(self, base_dict: dict = {}):
        main_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return main_dict | base_dict
