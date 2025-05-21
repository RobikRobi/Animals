from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.AnimalModel import Animal
from src.animals.animals_shema import AddAnimal
from src.db import get_session

app = APIRouter(prefix="/animals", tags=["Animals"])

@app.post("/add")
async def register_user(data:AddAnimal , session:AsyncSession = Depends(get_session)):
    newAnimal = Animal(**data.model_dump())
    session.add(newAnimal)
    await session.commit()
    await session.refresh(newAnimal)
    
    return newAnimal