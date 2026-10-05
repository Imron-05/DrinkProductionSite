from pydantic import BaseModel, Field
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

# Схема для ОБНОВЛЕНИЯ категории
class CategoryUpdate(BaseModel):
    name: Optional[str] = None

# Схема для СОЗДАНИЯ напитка (что отправляем при создании)
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    volume: float = Field(ge=0)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    shelf_life: Optional[int] = Field(default=None, ge=1)
    category_id: Optional[int] = Field(default=None, description="ID категории напитка")

# Схема для ОБНОВЛЕНИЯ напитка
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    volume: Optional[float] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    shelf_life: Optional[int] = None
    category_id: Optional[int] = None

# Схема для ЧТЕНИЯ напитка (что возвращает сервер, включая id)
class ProductResponse(ProductCreate):
    id: int

class CategoryResponse(CategoryBase):
    id: int
    products: List[ProductResponse] = []

    class Config:
        from_attributes = True

# Схема для входных данных при регистрации (принимает чистый пароль)
class UserCreate(BaseModel):
    username: str
    password: str

# Схема для ответа клиенту (НИКОГДА не возвращает пароль!)
class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True