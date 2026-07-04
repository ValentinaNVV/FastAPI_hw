from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from SQLAlchemy_hw import Connection, Brand, Product, BaseModel, ProductDTO
from pydantic import BaseModel as PydanticModel
from sqlalchemy import func

# Подключаемся к базе данных SQLite
conn = Connection("sqlite:///my_database.db")

# Создаём экземпляр FastAPI — это наш сервер
app = FastAPI()


# Инициализация кэша при запуске сервера
@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


# Проверка что сервер работает
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# GET /brands — возвращает список всех брендов из базы
@app.get("/brands")
def get_brands():
    brands = conn.session.query(Brand).all()
    return [{"id": brand.id, "name": brand.name} for brand in brands]


# GET /products/ — возвращает список всех товаров (с кэшем на 60 секунд)
@app.get("/products/")
@cache(expire=60)
async def get_products():
    products = conn.session.query(Product).all()
    return [{"id": p.id, "title": p.title, "price": p.price} for p in products]


# GET /products/{id}/ — возвращает один товар по его id
@app.get("/products/{id}/")
def get_product(id: int):
    product = conn.session.query(Product).filter_by(id=id).first()
    if not product:
        return {"error": "Товар не найден"}
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price,
        "brand_id": product.brand_id,
        "category_id": product.category_id
    }


# GET /statistics/ — общее количество товаров в базе
@app.get("/statistics/")
async def get_statistics():
    total = conn.session.query(func.count(Product.id)).scalar()
    return {"total_products": total}


# Схема данных для обновления товара — принимает title и/или price
class ProductUpdate(PydanticModel):
    title: str = None
    price: float = None


# PUT /products/{id}/update — обновляет title и/или price товара по id
@app.put("/products/{id}/update")
def update_product(id: int, data: ProductUpdate):
    product = conn.session.query(Product).filter_by(id=id).first()
    if not product:
        return {"error": "Товар не найден"}
    if data.title:
        product.title = data.title
    if data.price:
        product.price = data.price
    conn.session.commit()
    return {"message": "Товар обновлён", "id": product.id, "title": product.title, "price": product.price}
