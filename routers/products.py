from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database.dependencies import get_current_admin
from database.models import User
from database import models, schemas
from database.connection import get_db

# Создаём роутер вместо app
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# 1. Получить все продукты
@router.get("/", response_model=List[schemas.ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    # Применяем фильтр по названию, если оно передано
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))

    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)

    # Применяем фильтр по цене, если она передана
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    # 2. Добавили проверку категории
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)

    products = query.offset(skip).limit(limit).all()
    return products

# 2. Создать продукт
@router.post("/", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate,
                   db: Session = Depends(get_db),
                   admin_user: User = Depends(get_current_admin)):
    if product.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 3. Получить один продукт
@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product

# 4. Обновить продукт
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int,
                   product: schemas.ProductUpdate,
                   db: Session = Depends(get_db),
                   admin_user: User = Depends(get_current_admin)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    if product.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

# 5. Удалить продукт
@router.delete("/{product_id}")
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   admin_user: User = Depends(get_current_admin)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    db.delete(product)
    db.commit()
    return {"message": f"Продукт с ID {product_id} успешно удалён"}

@router.patch("/{product_id}", response_model=schemas.ProductResponse)
def patch_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукт не найден!")

    if product.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product
