from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from models.client import Group
from schemas import GroupCreateSchema, GroupResponseSchema


class GroupService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, group_data: GroupCreateSchema) -> GroupResponseSchema:
        if not group_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_group = Group(**group_data.model_dump())
        self.db.add(db_group)
        await self.db.commit()
        await self.db.refresh(db_group)
        return GroupResponseSchema.model_validate(db_group)

    async def get_group(self, group_id: str) -> Optional[GroupResponseSchema]:
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        db_group = result.scalar_one_or_none()
        if not db_group:
            return None
        return GroupResponseSchema.model_validate(db_group)

    async def list_groups(self) -> List[GroupResponseSchema]:
        result = await self.db.execute(select(Group))
        groups = result.scalars().all()
        return [GroupResponseSchema.model_validate(g) for g in groups]

    async def update_group(self, group_id: str, group_data: GroupCreateSchema) -> GroupResponseSchema:
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        db_group = result.scalar_one_or_none()
        if not db_group:
            raise HTTPException(404, "Group not found")
        if not group_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_group.name = group_data.name
        await self.db.commit()
        await self.db.refresh(db_group)
        return GroupResponseSchema.model_validate(db_group)

    async def delete_group(self, group_id: str) -> None:
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        db_group = result.scalar_one_or_none()
        if not db_group:
            raise HTTPException(404, "Group not found")
        await self.db.delete(db_group)
        await self.db.commit()
