from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.AnimalModel import Animal
from src.animals.animals_shema import AddAnimal, OutAnimal
from src.db import get_session
from fastapi_filter import FilterDepends
from src.animals.animals_filter import AnimalsFilter

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import config


app = APIRouter(prefix="/animals", tags=["Animals"])

def send_email():
    smtp_server = config.env_data.SMTP_SERVER
    port = config.env_data.SMTP_PORT
    login = config.env_data.EMAIL_LOGIN
    password = config.env_data.EMAIL_PASSWORD
    sender_email = config.env_data.EMAIL_SENDER
    receiver_email = config.env_data.EMAIL_RECEIVER

    subject = "Новое животное добавлено"
    body = """
Здравствуйте!

Спасибо, что добавили новое животное на нашем сайте.

Ваша работа важна для нас.
"""
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    text_part = MIMEText(body, "plain")
    message.attach(text_part)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email отправлен успешно")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")

@app.post("/add", response_model=OutAnimal)
async def register_animal(
    data: AddAnimal,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    newAnimal = Animal(**data.model_dump())
    session.add(newAnimal)
    await session.commit()
    await session.refresh(newAnimal)

    # Запускаем задачу по отправке email
    background_tasks.add_task(send_email)

    return newAnimal

@app.get("/filter", response_model=list[OutAnimal])
async def get_animals(user_filter: AnimalsFilter = FilterDepends(AnimalsFilter), db: AsyncSession = Depends(get_session)):
    query = user_filter.filter(select(Animal)) 
    result = await db.execute(query)
    return result.scalars().all()

