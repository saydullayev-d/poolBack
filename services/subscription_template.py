from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from models.client import SubscriptionTemplate
from schemas import SubscriptionTemplateCreateSchema, SubscriptionTemplateResponseSchema


class SubscriptionTemplateService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_subscription_template(self, template_data: SubscriptionTemplateCreateSchema) -> SubscriptionTemplateResponseSchema:
        if not template_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_template = SubscriptionTemplate(**template_data.model_dump())
        self.db.add(db_template)
        await self.db.commit()
        await self.db.refresh(db_template)
        return SubscriptionTemplateResponseSchema.model_validate(db_template)

    async def get_subscription_template(self, template_id: str) -> Optional[SubscriptionTemplateResponseSchema]:
        result = await self.db.execute(select(SubscriptionTemplate).filter(SubscriptionTemplate.id == template_id))
        db_template = result.scalar_one_or_none()
        if not db_template:
            return None
        return SubscriptionTemplateResponseSchema.model_validate(db_template)

    async def list_subscription_templates(self) -> List[SubscriptionTemplateResponseSchema]:
        result = await self.db.execute(select(SubscriptionTemplate))
        templates = result.scalars().all()
        return [SubscriptionTemplateResponseSchema.model_validate(t) for t in templates]

    async def update_subscription_template(self, template_id: str, template_data: SubscriptionTemplateCreateSchema) -> SubscriptionTemplateResponseSchema:
        result = await self.db.execute(select(SubscriptionTemplate).filter(SubscriptionTemplate.id == template_id))
        db_template = result.scalar_one_or_none()
        if not db_template:
            raise HTTPException(404, "SubscriptionTemplate not found")
        if not template_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")
        db_template.name = template_data.name
        await self.db.commit()
        await self.db.refresh(db_template)
        return SubscriptionTemplateResponseSchema.model_validate(db_template)

    async def delete_subscription_template(self, template_id: str) -> None:
        result = await self.db.execute(select(SubscriptionTemplate).filter(SubscriptionTemplate.id == template_id))
        db_template = result.scalar_one_or_none()
        if not db_template:
            raise HTTPException(404, "SubscriptionTemplate not found")
        await self.db.delete(db_template)
        await self.db.commit()
