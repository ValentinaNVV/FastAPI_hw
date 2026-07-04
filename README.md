# FastAPI Products API

API сервер на FastAPI для работы с товарами из базы данных SQLite.
Данные загружены из [DummyJSON](https://dummyjson.com/).

## Описание

Реализованы три эндпоинта для работы с товарами и брендами из базы данных, 
построенной в проекте SQLAlchemy.

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | /brands | Получение всех брендов |
| GET | /products/{id}/ | Получение товара по id |
| PUT | /products/{id}/update | Обновление товара по id |

## Как запустить

1. Установить зависимости:
```bash
pip install fastapi uvicorn sqlalchemy
```

2. Запустить сервер:
```bash
uvicorn main:app --reload --port 8001
```

3. Открыть в браузере:
- API: `http://127.0.0.1:8001`
- Документация: `http://127.0.0.1:8001/docs`
