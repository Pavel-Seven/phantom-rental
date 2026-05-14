FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь наш код в контейнер
COPY . .

# Запускаем сервер, используя порт, который выдаст облако (или 8000 по умолчанию)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
