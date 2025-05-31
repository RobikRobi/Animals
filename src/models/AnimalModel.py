from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base

class Animal(Base):
    __tablename__ = "animal_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]
    description:Mapped[str]
    population:Mapped[int]

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description":self.description,
            "population":self.population
        }