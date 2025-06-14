import logging
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.AnimalModel import Animal
from src.animals.animals_shema import AddAnimal, OutAnimal
from src.db import get_session
from fastapi_filter import FilterDepends
from src.animals.animals_filter import AnimalsFilter
from src.tasks.email_tasks import send_email_task

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import config

from src.redis_client import redis_client
import json

app = APIRouter(prefix="/animals", tags=["Animals"])

logger = logging.getLogger(__name__)

# # функция отправки сообщения
# def send_email(email_receiver: str):
#     smtp_server = config.env_data.SMTP_SERVER
#     port = config.env_data.SMTP_PORT
#     login = config.env_data.EMAIL_LOGIN
#     password = config.env_data.EMAIL_PASSWORD
#     sender_email = config.env_data.EMAIL_SENDER
#     receiver_email = email_receiver

#     subject = "Новое животное добавлено"
#     body = """
# Здравствуйте!

# Спасибо, что добавили новое животное на нашем сайте.

# Ваша работа важна для нас.
# """
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject
#     message["From"] = sender_email
#     message["To"] = receiver_email

#     text_part = MIMEText(body, "plain")
#     message.attach(text_part)

#     try:
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.starttls()
#             server.login(login, password)
#             server.sendmail(sender_email, receiver_email, message.as_string())
#         print("Email отправлен успешно")
#     except Exception as e:
#         print(f"Ошибка при отправке email: {e}")

# добавление данных в базу
@app.post("/add", response_model=OutAnimal)
async def register_animal(
    data: AddAnimal,
    email_receiver: str,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    newAnimal = Animal(**data.model_dump())
    session.add(newAnimal)
    await session.commit()
    await session.refresh(newAnimal)

    send_email_task.delay(email_receiver)

    # # Запускаем задачу по отправке email
    # background_tasks.add_task(send_email, email_receiver)

    # Делаем логирование
    logger.info(f"Добавлено животное: {newAnimal}")
    logger.info(f"Email отправлен на: {email_receiver}")

    return newAnimal

# фильтрация данных
@app.get("/filter", response_model=list[OutAnimal])
async def get_animals(user_filter: AnimalsFilter = FilterDepends(AnimalsFilter), db: AsyncSession = Depends(get_session)):
    query = user_filter.filter(select(Animal)) 
    result = await db.execute(query)
    return result.scalars().all()

# кэширование базы данных
@app.get("/cache", response_model=list[OutAnimal])
async def get_animals(session: AsyncSession = Depends(get_session)):
    cache_key = "animals_list"
    cached_data = await redis_client.get(cache_key)
    
    if cached_data:
        print("Данные взяты из кэша")
        return json.loads(cached_data)
    
    # Если в кэше нет — запросим из базы
    result = await session.execute(select(Animal))
    animals = result.scalars().all()

    await redis_client.set(cache_key, json.dumps([animal.as_dict() for animal in animals]), ex=60)

    return [animal.as_dict() for animal in animals]

# очистка кэша
@app.post("/clear_cache")
async def clear_cache():
    await redis_client.delete("animals_list")
    return {"status": "Кэш очищен"}