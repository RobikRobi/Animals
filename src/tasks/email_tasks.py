from src.worker import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import config

@celery_app.task(name="send_email_task")  # 👈 имя без модуля
def send_email_task(email_receiver: str):
    smtp_server = config.env_data.SMTP_SERVER
    port = config.env_data.SMTP_PORT
    login = config.env_data.EMAIL_LOGIN
    password = config.env_data.EMAIL_PASSWORD
    sender_email = config.env_data.EMAIL_SENDER

    subject = "Новое животное добавлено"
    body = """
Здравствуйте!

Спасибо, что добавили новое животное на нашем сайте.

Ваша работа важна для нас.
"""
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email_receiver
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, email_receiver, message.as_string())
        print("Email отправлен успешно")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")