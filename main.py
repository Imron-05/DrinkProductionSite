import uvicorn
from fastapi import FastAPI
from database import models
from database.connection import engine
from routers import products, categories, auth



# Создаём таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Завод Напитков API")

# Подключаем наш роутер
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

