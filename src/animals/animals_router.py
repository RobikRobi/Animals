from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.AnimalModel import Animal
from src.animals.animals_shema import AddAnimal, OutAnimal
from src.db import get_session
from fastapi_filter import FilterDepends, with_prefix
from src.animals.animals_filter import AnimalsFilter

app = APIRouter(prefix="/animals", tags=["Animals"])

@app.post("/add")
async def register_user(data:AddAnimal , session:AsyncSession = Depends(get_session)):
    newAnimal = Animal(**data.model_dump())
    session.add(newAnimal)
    await session.commit()
    await session.refresh(newAnimal)
    
    return newAnimal

@app.get("/filter", response_model=list[OutAnimal])
async def get_animals(user_filter: AnimalsFilter = FilterDepends(AnimalsFilter), db: AsyncSession = Depends(get_session)):
    query = user_filter.filter(select(Animal)) 
    result = await db.execute(query)
    return result.scalars().all()