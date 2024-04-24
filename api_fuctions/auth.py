from email.mime.text import MIMEText
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.tables import Users
from fastapi import HTTPException
import secrets
import smtplib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_token():
    """
    Функция генерирует и возвращает токен
    """
    return secrets.token_hex(16)


def token_verify(token: str, db: Session) -> dict:
    """
    Функция для получения id и username пользователя по токену.

    Args:
    token (str): Токен пользователя для поиска.
    db (Session): Сессия базы данных.

    Returns:
    dict: Словарь с id и username пользователя или сообщение об ошибке.
    """
    user = db.query(Users).filter(Users.token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid token")

    return {"id": user.id, "username": user.username}


# Подключение к серверу SMTP для отправки электронных писем
def send_email(receiver_email: str, subject: str, message: str):
    sender_email = "obsudim.7@mail.ru"
    password = "MySAWsLx6WkitzCanTay"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
