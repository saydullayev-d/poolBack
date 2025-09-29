from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.database import get_db
from services.subscription import SubscriptionService
from schemas import Subscription, SubscriptionCreate

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/", response_model=Subscription)
async def create_subscription(data: SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    return await SubscriptionService(db).create_subscription(data)


@router.get("/{subscription_id}", response_model=Subscription)
async def get_subscription(subscription_id: str, db: AsyncSession = Depends(get_db)):
    sub = await SubscriptionService(db).get_subscription(subscription_id)
    if not sub:
        raise HTTPException(404, "Subscription not found")
    return sub


@router.get("/", response_model=List[Subscription])
async def list_subscriptions(db: AsyncSession = Depends(get_db)):
    return await SubscriptionService(db).list_subscriptions()


@router.put("/{subscription_id}", response_model=Subscription)
async def update_subscription(subscription_id: str, data: SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    return await SubscriptionService(db).update_subscription(subscription_id, data)


@router.delete("/{subscription_id}")
async def delete_subscription(subscription_id: str, db: AsyncSession = Depends(get_db)):
    await SubscriptionService(db).delete_subscription(subscription_id)
    return {"message": "Subscription deleted"}
