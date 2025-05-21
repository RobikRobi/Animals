from pydantic import BaseModel

class AddAnimal(BaseModel):

    name: str
    description: str
    population: int