from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.auth import get_current_user
from app.models import User
from app.services import RelationService
from app.schemas import RelationCreateSchema, RelationResponseSchema
from ..dependencies import get_relation_service

router = APIRouter(prefix="/relations", tags=["relations"])

@router.post("", response_model=RelationResponseSchema)
async def create_relation(relation_data: RelationCreateSchema, service: RelationService = Depends(get_relation_service), current_user: User = Depends(get_current_user)):
    return await service.create_relation(relation_data)

@router.get("/{relation_id}", response_model=RelationResponseSchema)
async def get_relation(relation_id: str, service: RelationService = Depends(get_relation_service), current_user: User = Depends(get_current_user)):
    relation = await service.get_relation(relation_id)
    if not relation:
        raise HTTPException(404, "Relation not found")
    return relation

@router.get("", response_model=List[RelationResponseSchema])
async def list_relations(service: RelationService = Depends(get_relation_service), current_user: User = Depends(get_current_user)):
    return await service.list_relations()

@router.put("/{relation_id}", response_model=RelationResponseSchema)
async def update_relation(relation_id: str, relation_data: RelationCreateSchema, service: RelationService = Depends(get_relation_service), current_user: User = Depends(get_current_user)):
    return await service.update_relation(relation_id, relation_data)

@router.delete("/{relation_id}")
async def delete_relation(relation_id: str, service: RelationService = Depends(get_relation_service), current_user: User = Depends(get_current_user)):
    await service.delete_relation(relation_id)
    return {"message": "Relation deleted"}
