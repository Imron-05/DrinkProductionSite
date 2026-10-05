from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import schemas
from database.dependencies import get_current_admin
from database.connection import get_db
from database.models import Category, User
from database.schemas import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate,
                    db: Session = Depends(get_db),
                    admin_user: User = Depends(get_current_admin)
                    ):
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Категория с таким именем уже существует")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int,
                    db: Session = Depends(get_db),
                    admin_user: User = Depends(get_current_admin)
                    ):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    db.delete(category)
    db.commit()
    return {"message": f"Категория с ID {category_id} успешно удалена"}

# Обновление категории (только для админа)
@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    if category.name is not None:
        db_category.name = category.name

    db.commit()
    db.refresh(db_category)
    return db_category
