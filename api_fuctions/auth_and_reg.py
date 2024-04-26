from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
import secrets
from pydantic_models.users import Creds, Reg
from database.functional import *
import uuid
from starlette.responses import Response

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
# def send_email(receiver_email: str, subject: str, message: str):
#     sender_email = "obsudim.7@mail.ru"
#     password = "MySAWsLx6WkitzCanTay"
# 
#     msg = MIMEText(message)
#     msg['Subject'] = subject
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
# 
#     server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     server.quit()


# def get_users(access_token) -> list or str:
#     if not access_token:
#         return "not token"
#     token_data = token_verify(access_token)
#
#     if token_data == 'Token has expired':
#         return "Token has expired"
#     elif token_data == 'Invalid token':
#         return "Invalid token"
#
#     role = check_role(uuid.UUID(token_data['user_id']))
#
#     if role == 0:
#         items = get_all_users()
#         return items
#     else:
#         return "access denied"

def authorization(creds_model: Creds, response: Response):
    if check_user(creds_model.email, creds_model.password) == 0:
        token = generate_token()
        # response.set_cookie(key="access_token", value=token, httponly=True) # эта чё
        return token
    else:
        return "Invalid password or login"


def register(reg_model: Reg) -> str:
    # TODO: Сделать проверку юзернейма пользователя. Одинаковых быть не должно
    if reg_model.password == reg_model.confirm_password:
        if register_user_to_db(reg_model.username, reg_model.email, reg_model.password) == 0:
            return "Successfully"
        else:
            return "A user with this email address has already been registered"
    else:
        return "Password or Login mismatch"
