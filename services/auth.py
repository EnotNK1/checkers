import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText


# Функция для генерации JWT токена
def generate_token(user_id):
    # Установка срока действия токена (1 час)
    expiry = datetime.utcnow() + timedelta(hours=1)

    # Создание токена с идентификатором пользователя и сроком действия
    token = jwt.encode({'user_id': str(user_id), 'exp': expiry}, 'secret_key', algorithm='HS256')

    return token


# Функция для проверки JWT токена
def verify_token(token):
    try:
        # Проверка токена и декодирование его содержимого
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Обработка исключения при истечении срока действия токена
        return 'Token has expired'
    except jwt.InvalidTokenError:
        # Обработка других недопустимых токенов
        return 'Invalid token'


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
