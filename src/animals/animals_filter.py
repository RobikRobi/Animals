from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from src.models.AnimalModel import Animal

class AnimalsFilter(Filter):
    name__ilike: str | None = None
    description__like: str | None = None
    population__gte: int | None = None
    population__lte: int | None = None
    population__in: list[int] | None = None

    class Constants(Filter.Constants):
        model = Animal

