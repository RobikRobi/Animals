from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from src.models.AnimalModel import Animal

class AnimalsFilter(Filter):
    name__ilike: Optional[str] = None
    description__like: Optional[str] = None
    population__gte: Optional[int] = None
    population__lte: Optional[int] = None
    population__in: Optional[list[int]] = None

    class Constants(Filter.Constants):
        model = Animal

