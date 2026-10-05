from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.connection import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    # Связь: одна категория содержит много продуктов
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Название напитка
    volume = Column(Float)  # Объём (например, 0.5)
    price = Column(Float)  # Цена
    quantity = Column(Integer, default=0)  # Количество на складе
    shelf_life = Column(Integer, nullable=True)  # Срок годности

    # Внешний ключ на категорию
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Связь обратная к категории
    category = relationship("Category", back_populates="products")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)  # True — админ, False — обычный юзер