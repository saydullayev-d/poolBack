from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from models.subscription import Subscription
from schemas import SubscriptionCreate, Subscription as SubscriptionSchema


class SubscriptionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_subscription(self, subscription_data: SubscriptionCreate) -> SubscriptionSchema:
        if not subscription_data.subscription_number.strip():
            raise HTTPException(400, "Subscription number cannot be empty")

        db_subscription = Subscription(**subscription_data.model_dump())
        self.db.add(db_subscription)
        await self.db.commit()
        await self.db.refresh(db_subscription)
        return SubscriptionSchema.model_validate(db_subscription)

    async def get_subscription(self, subscription_id: str) -> Optional[SubscriptionSchema]:
        result = await self.db.execute(select(Subscription).filter(Subscription.id == subscription_id))
        db_subscription = result.scalar_one_or_none()
        if not db_subscription:
            return None
        return SubscriptionSchema.model_validate(db_subscription)

    async def list_subscriptions(self) -> List[SubscriptionSchema]:
        result = await self.db.execute(select(Subscription))
        subscriptions = result.scalars().all()
        return [SubscriptionSchema.model_validate(s) for s in subscriptions]

    async def update_subscription(self, subscription_id: str, subscription_data: SubscriptionCreate) -> SubscriptionSchema:
        result = await self.db.execute(select(Subscription).filter(Subscription.id == subscription_id))
        db_subscription = result.scalar_one_or_none()
        if not db_subscription:
            raise HTTPException(404, "Subscription not found")

        if not subscription_data.subscription_number.strip():
            raise HTTPException(400, "Subscription number cannot be empty")

        for field, value in subscription_data.model_dump().items():
            setattr(db_subscription, field, value)

        await self.db.commit()
        await self.db.refresh(db_subscription)
        return SubscriptionSchema.model_validate(db_subscription)

    async def delete_subscription(self, subscription_id: str) -> None:
        result = await self.db.execute(select(Subscription).filter(Subscription.id == subscription_id))
        db_subscription = result.scalar_one_or_none()
        if not db_subscription:
            raise HTTPException(404, "Subscription not found")

        await self.db.delete(db_subscription)
        await self.db.commit()
