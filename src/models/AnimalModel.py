import typing

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


from src.db import Base

class Animal(Base):
    __tablename__ = "animal_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]
    description:Mapped[str]
    population:Mapped[int]