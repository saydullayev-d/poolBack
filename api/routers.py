from fastapi import APIRouter, Depends, HTTPException
from services import ClientService, RelationService, DiagnosisService, GroupService, SubscriptionTemplateService
from .schemas import (
    ClientCreateSchema, ClientResponseSchema,
    RelationCreateSchema, RelationResponseSchema,
    DiagnosisCreateSchema, DiagnosisResponseSchema,
    GroupCreateSchema, GroupResponseSchema,
    SubscriptionTemplateCreateSchema, SubscriptionTemplateResponseSchema
)
from .dependencies import (
    get_client_service, get_relation_service, get_diagnosis_service,
    get_group_service, get_subscription_template_service
)
from typing import List

router = APIRouter(tags=["api"])

# Client Endpoints
@router.post("/clients", response_model=ClientResponseSchema)
async def create_client(client_data: ClientCreateSchema, service: ClientService = Depends(get_client_service)):
    return await service.create_client(client_data)

@router.get("/clients/{client_id}", response_model=ClientResponseSchema)
async def get_client(client_id: str, service: ClientService = Depends(get_client_service)):
    client = await service.get_client(client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    return client

@router.get("/clients", response_model=List[ClientResponseSchema])
async def list_clients(service: ClientService = Depends(get_client_service)):
    return await service.list_clients()

@router.put("/clients/{client_id}", response_model=ClientResponseSchema)
async def update_client(client_id: str, client_data: ClientCreateSchema, service: ClientService = Depends(get_client_service)):
    return await service.update_client(client_id, client_data)

@router.delete("/clients/{client_id}")
async def delete_client(client_id: str, service: ClientService = Depends(get_client_service)):
    await service.delete_client(client_id)
    return {"message": "Client deleted"}

# Relation Endpoints
@router.post("/relations", response_model=RelationResponseSchema)
async def create_relation(relation_data: RelationCreateSchema, service: RelationService = Depends(get_relation_service)):
    return await service.create_relation(relation_data)

@router.get("/relations/{relation_id}", response_model=RelationResponseSchema)
async def get_relation(relation_id: str, service: RelationService = Depends(get_relation_service)):
    relation = await service.get_relation(relation_id)
    if not relation:
        raise HTTPException(404, "Relation not found")
    return relation

@router.get("/relations", response_model=List[RelationResponseSchema])
async def list_relations(service: RelationService = Depends(get_relation_service)):
    return await service.list_relations()

@router.put("/relations/{relation_id}", response_model=RelationResponseSchema)
async def update_relation(relation_id: str, relation_data: RelationCreateSchema, service: RelationService = Depends(get_relation_service)):
    return await service.update_relation(relation_id, relation_data)

@router.delete("/relations/{relation_id}")
async def delete_relation(relation_id: str, service: RelationService = Depends(get_relation_service)):
    await service.delete_relation(relation_id)
    return {"message": "Relation deleted"}

# Diagnosis Endpoints
@router.post("/diagnoses", response_model=DiagnosisResponseSchema)
async def create_diagnosis(diagnosis_data: DiagnosisCreateSchema, service: DiagnosisService = Depends(get_diagnosis_service)):
    return await service.create_diagnosis(diagnosis_data)

@router.get("/diagnoses/{diagnosis_id}", response_model=DiagnosisResponseSchema)
async def get_diagnosis(diagnosis_id: str, service: DiagnosisService = Depends(get_diagnosis_service)):
    diagnosis = await service.get_diagnosis(diagnosis_id)
    if not diagnosis:
        raise HTTPException(404, "Diagnosis not found")
    return diagnosis

@router.get("/diagnoses", response_model=List[DiagnosisResponseSchema])
async def list_diagnoses(service: DiagnosisService = Depends(get_diagnosis_service)):
    return await service.list_diagnoses()

@router.put("/diagnoses/{diagnosis_id}", response_model=DiagnosisResponseSchema)
async def update_diagnosis(diagnosis_id: str, diagnosis_data: DiagnosisCreateSchema, service: DiagnosisService = Depends(get_diagnosis_service)):
    return await service.update_diagnosis(diagnosis_id, diagnosis_data)

@router.delete("/diagnoses/{diagnosis_id}")
async def delete_diagnosis(diagnosis_id: str, service: DiagnosisService = Depends(get_diagnosis_service)):
    await service.delete_diagnosis(diagnosis_id)
    return {"message": "Diagnosis deleted"}

# Group Endpoints
@router.post("/groups", response_model=GroupResponseSchema)
async def create_group(group_data: GroupCreateSchema, service: GroupService = Depends(get_group_service)):
    return await service.create_group(group_data)

@router.get("/groups/{group_id}", response_model=GroupResponseSchema)
async def get_group(group_id: str, service: GroupService = Depends(get_group_service)):
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    return group

@router.get("/groups", response_model=List[GroupResponseSchema])
async def list_groups(service: GroupService = Depends(get_group_service)):
    return await service.list_groups()

@router.put("/groups/{group_id}", response_model=GroupResponseSchema)
async def update_group(group_id: str, group_data: GroupCreateSchema, service: GroupService = Depends(get_group_service)):
    return await service.update_group(group_id, group_data)

@router.delete("/groups/{group_id}")
async def delete_group(group_id: str, service: GroupService = Depends(get_group_service)):
    await service.delete_group(group_id)
    return {"message": "Group deleted"}

# SubscriptionTemplate Endpoints
@router.post("/subscription_templates", response_model=SubscriptionTemplateResponseSchema)
async def create_subscription_template(template_data: SubscriptionTemplateCreateSchema, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    return await service.create_subscription_template(template_data)

@router.get("/subscription_templates/{template_id}", response_model=SubscriptionTemplateResponseSchema)
async def get_subscription_template(template_id: str, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    template = await service.get_subscription_template(template_id)
    if not template:
        raise HTTPException(404, "SubscriptionTemplate not found")
    return template

@router.get("/subscription_templates", response_model=List[SubscriptionTemplateResponseSchema])
async def list_subscription_templates(service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    return await service.list_subscription_templates()

@router.put("/subscription_templates/{template_id}", response_model=SubscriptionTemplateResponseSchema)
async def update_subscription_template(template_id: str, template_data: SubscriptionTemplateCreateSchema, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    return await service.update_subscription_template(template_id, template_data)

@router.delete("/subscription_templates/{template_id}")
async def delete_subscription_template(template_id: str, service: SubscriptionTemplateService = Depends(get_subscription_template_service)):
    await service.delete_subscription_template(template_id)
    return {"message": "SubscriptionTemplate deleted"}