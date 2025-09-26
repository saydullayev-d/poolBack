from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services import SubscriptionTemplateService
from schemas import SubscriptionTemplateCreateSchema, SubscriptionTemplateResponseSchema
from ..dependencies import get_subscription_template_service

router = APIRouter(prefix="/subscription_templates", tags=["subscription_templates"])

@router.post("", response_model=SubscriptionTemplateResponseSchema)
async def create_subscription_template(template_data: SubscriptionTemplateCreateSchema, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    return await service.create_subscription_template(template_data)

@router.get("/{template_id}", response_model=SubscriptionTemplateResponseSchema)
async def get_subscription_template(template_id: str, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    template = await service.get_subscription_template(template_id)
    if not template:
        raise HTTPException(404, "SubscriptionTemplate not found")
    return template

@router.get("", response_model=List[SubscriptionTemplateResponseSchema])
async def list_subscription_templates(service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    return await service.list_subscription_templates()

@router.put("/{template_id}", response_model=SubscriptionTemplateResponseSchema)
async def update_subscription_template(template_id: str, template_data: SubscriptionTemplateCreateSchema, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    return await service.update_subscription_template(template_id, template_data)

@router.delete("/{template_id}")
async def delete_subscription_template(template_id: str, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    await service.delete_subscription_template(template_id)
    return {"message": "SubscriptionTemplate deleted"}
