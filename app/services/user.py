from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class UsersService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(name=user.name, password=hashed_password, role=user.role)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_users(self):
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_user(self, user_id: str, user: UserCreate):
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None
        db_user.name = user.name
        db_user.password = get_password_hash(user.password)
        db_user.role = user.role
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: str) -> Optional[User]:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None
        await self.db.delete(db_user)
        await self.db.commit()
        return db_user
