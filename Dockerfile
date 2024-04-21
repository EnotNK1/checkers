# Используем базовый образ Python
FROM python:3.9

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Копируем исходный код приложения в образ
COPY . /app

# Определяем переменные окружения для подключения к PostgreSQL
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=dbname
ENV POSTGRES_HOST=db

# Запускаем приложение
CMD gunicorn main:app --bind=0.0.0.0:8080
#CMD ["python", "main.py"]