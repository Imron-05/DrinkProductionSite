from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Конфигурация шифрования паролей (используем алгоритм bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ для подписи JWT-токенов (в бэкенде это "пароль от всех дверей")
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Токен живёт 30 минут


# 1. Функция хэширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 2. Функция проверки пароля (сравнивает чистый пароль с хэшем из БД)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 3. Функция создания JWT-токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
