from enum import Enum
from typing import List

import sqlalchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ActionType(Enum):
    DELETE = 0
    REPORT = 1
    COMMENT = 2


class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    type: Mapped[ActionType] = mapped_column(sqlalchemy.Enum(ActionType))
    content: Mapped[str] = mapped_column(String(200), nullable=True)


class KeywordList(Base):
    __tablename__ = "keyword_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    words: Mapped[List["Keyword"]] = relationship()


class Keyword(Base):
    __tablename__ = "keyword"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("keyword_list.id"))
