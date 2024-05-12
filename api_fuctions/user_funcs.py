from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
import secrets
from pydantic_models.users import *
from database.functional import *

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


def authorization(creds_model: Creds):
    db = s()
    if check_user(creds_model.email, creds_model.password) == 0:
        token = generate_token()
        user = db.query(Users).filter_by(email=creds_model.email).first()
        if user:
            user.token = token
            db.commit()
        return token
    else:
        return "Invalid password or login"


def register(reg_model: Reg) -> str:
    if username_exists_in_db(reg_model.username):
        return "Username already taken"

    if reg_model.password == reg_model.confirm_password:
        if register_user_to_db(reg_model.username, reg_model.email, reg_model.password) == 0:
            return "Successfully"
        else:
            return "A user with this email address has already been registered"
    else:
        return "Password or Login mismatch"


def get_userdata_from_token(token: str):
    # Создаем сессию
    session = s()
    try:
        # Ищем пользователя по токену
        user = session.query(Users).filter(Users.token == token).first()
        # Возвращаем данные пользователя, если он найден
        if user is not None:
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password  # Обычно пароль не возвращают!
            }
        else:
            return None
    finally:
        session.close()


def username_change(new_username: str, token: Token):
    db = s()
    user = db.query(Users).filter(Users.token == token.token).first()
    if user:
        if user.username != new_username:
            user.username = new_username
            db.commit()
            return True  # Indicates successful change
        else:
            return True  # No change needed, but not an error
    else:
        return False  # Indicates user not found and no update was made
