from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from models.client import Relation
from schemas import RelationCreateSchema, RelationResponseSchema


class RelationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_relation(self, relation_data: RelationCreateSchema) -> RelationResponseSchema:
        if not relation_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_relation = Relation(**relation_data.model_dump())
        self.db.add(db_relation)
        await self.db.commit()
        await self.db.refresh(db_relation)
        return RelationResponseSchema.model_validate(db_relation)

    async def get_relation(self, relation_id: str) -> Optional[RelationResponseSchema]:
        result = await self.db.execute(select(Relation).filter(Relation.id == relation_id))
        db_relation = result.scalar_one_or_none()
        if not db_relation:
            return None
        return RelationResponseSchema.model_validate(db_relation)

    async def list_relations(self) -> List[RelationResponseSchema]:
        result = await self.db.execute(select(Relation))
        relations = result.scalars().all()
        return [RelationResponseSchema.model_validate(r) for r in relations]

    async def update_relation(self, relation_id: str, relation_data: RelationCreateSchema) -> RelationResponseSchema:
        result = await self.db.execute(select(Relation).filter(Relation.id == relation_id))
        db_relation = result.scalar_one_or_none()
        if not db_relation:
            raise HTTPException(404, "Relation not found")
        if not relation_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_relation.name = relation_data.name
        await self.db.commit()
        await self.db.refresh(db_relation)
        return RelationResponseSchema.model_validate(db_relation)

    async def delete_relation(self, relation_id: str) -> None:
        result = await self.db.execute(select(Relation).filter(Relation.id == relation_id))
        db_relation = result.scalar_one_or_none()
        if not db_relation:
            raise HTTPException(404, "Relation not found")
        await self.db.delete(db_relation)
        await self.db.commit()
