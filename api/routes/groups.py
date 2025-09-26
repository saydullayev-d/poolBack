from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services import GroupService
from schemas import GroupCreateSchema, GroupResponseSchema
from ..dependencies import get_group_service

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("", response_model=GroupResponseSchema)
async def create_group(group_data: GroupCreateSchema, service: GroupService = Depends(get_group_service)):
    return await service.create_group(group_data)

@router.get("/{group_id}", response_model=GroupResponseSchema)
async def get_group(group_id: str, service: GroupService = Depends(get_group_service)):
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    return group

@router.get("", response_model=List[GroupResponseSchema])
async def list_groups(service: GroupService = Depends(get_group_service)):
    return await service.list_groups()

@router.put("/{group_id}", response_model=GroupResponseSchema)
async def update_group(group_id: str, group_data: GroupCreateSchema, service: GroupService = Depends(get_group_service)):
    return await service.update_group(group_id, group_data)

@router.delete("/{group_id}")
async def delete_group(group_id: str, service: GroupService = Depends(get_group_service)):
    await service.delete_group(group_id)
    return {"message": "Group deleted"}
