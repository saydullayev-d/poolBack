from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.models.database import get_db
from app.models.user import User

# --------------------------------------------------------------------
# Конфиг
# --------------------------------------------------------------------
SECRET_KEY = "Y_unyhC7aiRLtnVkYjTA9fC-LHr_ElxY9Znb95amuFQ"  # вынеси в .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# --------------------------------------------------------------------
# Pydantic модель для токена
# --------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


# --------------------------------------------------------------------
# Хэш пароля
# --------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# --------------------------------------------------------------------
# Получение пользователя по name (логин = name)
# --------------------------------------------------------------------
async def get_user_by_name(name: str, db: AsyncSession) -> Optional[User]:
    stmt = select(User).where(User.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()


# --------------------------------------------------------------------
# Аутентификация
# --------------------------------------------------------------------
async def authenticate_user(name: str, password: str, db: AsyncSession):
    user = await get_user_by_name(name, db)
    if not user or not verify_password(password, user.password):
        return None
    return user


# --------------------------------------------------------------------
# JWT токен
# --------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --------------------------------------------------------------------
# Получение текущего пользователя из токена
# --------------------------------------------------------------------
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_name(name, db)
    if user is None:
        raise credentials_exception

    return user

