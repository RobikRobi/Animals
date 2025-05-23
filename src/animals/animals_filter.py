from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from src.models.AnimalModel import Animal

class AnimalsFilter(Filter):
    name: Optional[str]
    description: Optional[str] = None
    population: Optional[int] = None

    class Constants(Filter.Constants):
        model = Animal

