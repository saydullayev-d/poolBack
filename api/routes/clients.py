from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services import ClientService
from schemas import ClientCreateSchema, ClientResponseSchema
from ..dependencies import get_client_service

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientResponseSchema)
async def create_client(client_data: ClientCreateSchema, service: ClientService = Depends(get_client_service)):
    return await service.create_client(client_data)

@router.get("/{client_id}", response_model=ClientResponseSchema)
async def get_client(client_id: str, service: ClientService = Depends(get_client_service)):
    client = await service.get_client(client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    return client

@router.get("/", response_model=List[ClientResponseSchema])
async def list_clients(service: ClientService = Depends(get_client_service)):
    clients = await service.list_clients()
    if not clients:
        raise HTTPException(404, "Clients not found")
    return clients

@router.put("/{client_id}", response_model=ClientResponseSchema)
async def update_client(client_id: str, client_data: ClientCreateSchema, service: ClientService = Depends(get_client_service)):
    return await service.update_client(client_id, client_data)

@router.delete("/{client_id}")
async def delete_client(client_id: str, service: ClientService = Depends(get_client_service)):
    await service.delete_client(client_id)
    return {"message": "Client deleted"}
