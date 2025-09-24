from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_db
from services import ClientService, RelationService, DiagnosisService, GroupService, SubscriptionTemplateService

async def get_client_service(db: AsyncSession = Depends(get_db)) -> ClientService:
    return ClientService(db)

async def get_relation_service(db: AsyncSession = Depends(get_db)) -> RelationService:
    return RelationService(db)

async def get_diagnosis_service(db: AsyncSession = Depends(get_db)) -> DiagnosisService:
    return DiagnosisService(db)

async def get_group_service(db: AsyncSession = Depends(get_db)) -> GroupService:
    return GroupService(db)

async def get_subscription_template_service(db: AsyncSession = Depends(get_db)) -> SubscriptionTemplateService:
    return SubscriptionTemplateService(db)