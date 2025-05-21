from fastapi import FastAPI

from src.db import engine,Base
from binascii import Error
from fastapi.middleware.cors import CORSMiddleware


# from src.admin_panel.admin_router import app as admin_app

from src.models.AnimalModel import Animal

from src.animals.animals_router import app as animal_app



app = FastAPI()

# routers
app.include_router(animal_app)

@app.get("/init")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)     
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"db creat! =)"})


origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)