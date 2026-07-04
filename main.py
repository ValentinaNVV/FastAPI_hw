from fastapi import FastAPI
from SQLAlchemy_hw import Connection, Brand, Product, BaseModel, ProductDTO
from pydantic import BaseModel as PydanticModel

# Подключаемся к базе данных SQLite
conn = Connection("sqlite:///my_database.db")

# Создаём экземпляр FastAPI — это наш сервер
app = FastAPI()


# Проверка что сервер работает
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# GET /brands — возвращает список всех брендов из базы
@app.get("/brands")
def get_brands():
    brands = conn.session.query(Brand).all()
    return [{"id": brand.id, "name": brand.name} for brand in brands]

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