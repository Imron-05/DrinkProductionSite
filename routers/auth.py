from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.dependencies import get_current_user
from database.auth import verify_password, get_password_hash,create_access_token
from database import models
from database.connection import get_db
from database.models import User
from database.schemas import UserCreate, UserResponse



router = APIRouter(prefix="/auth", tags=["auth"])


# Эндпоинт для проверки авторизованного пользователя
@router.get("/me", response_model=UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "is_admin": current_user.is_admin
    }

#1 "Эндпоинт регистрации нового пользователя
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже пользователя с таким именем
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем уже существует",
        )
#Хэшируем пароли и сохраним юзеров в бд
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        username = user_data.username,
        hashed_password = hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Ищем пользователя в бд
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}