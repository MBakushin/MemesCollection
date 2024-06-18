# Memes App

## Описание

Веб-приложение для работы с коллекцией мемов, предоставляющее API для добавления, обновления, удаления и получения мемов.

## Функциональность

- Получение списка всех мемов с пагинацией
- Получение конкретного мема по его ID
- Добавление нового мема с изображением и текстом
- Обновление существующего мема
- Удаление мема

## Запуск проекта

### Требования

- Docker
- Docker Compose

### Шаги

1. Клонируйте репозиторий:

    ```sh
    git clone git@github.com:MBakushin/MemesCollection.git
    cd MemesCollection
    ```

2. Создайте файл `.env` и добавьте следующие переменные:

    ```env
    SQLALCHEMY_DATABASE_URL=postgresql://user:password@db:5432/memes
    S3_ENDPOINT_URL=http://minio:9000
    S3_ACCESS_KEY=minioadmin
    S3_SECRET_KEY=minioadmin
    S3_BUCKET_NAME=memes
    ```

3. Запустите приложение с помощью Docker Compose:

    ```sh
    docker-compose up --build
    ```

## Документация API

После запуска приложения, документация API будет доступна по адресу:

http://localhost:8000/docs