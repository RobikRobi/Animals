from pydantic import BaseModel

class AddAnimal(BaseModel):

    name: str
    description: str
    population: int

class OutAnimal(BaseModel):

    name: str 
    description: str
    population: int