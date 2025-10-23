import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.auth import get_current_user
from app.models import User
from app.services import ClientService
from app.schemas import ClientCreateSchema, ClientResponseSchema
from ..dependencies import get_client_service, get_db
from pydantic import BaseModel


router = APIRouter(prefix="/clients", tags=["clients"])


class PhotoUploadResponse(BaseModel):
    message: str
    photo_path: str

@router.post("/", response_model=ClientResponseSchema)
async def create_client(
    client_data: ClientCreateSchema,
    service: ClientService = Depends(get_client_service), 
    current_user: User = Depends(get_current_user)
):
    return await service.create_client(client_data)


@router.get("/{client_id}", response_model=ClientResponseSchema)
async def get_client(
    client_id: str,
    service: ClientService = Depends(get_client_service), 
    current_user: User = Depends(get_current_user)
):
    client = await service.get_client(client_id)
    if not client:
        raise HTTPException(404, "Client not found")
    return client


@router.get("/", response_model=List[ClientResponseSchema])
async def list_clients(service: ClientService = Depends(get_client_service), current_user: User = Depends(get_current_user)):
    clients = await service.list_clients()
    if not clients:
        raise HTTPException(404, "Clients not found")
    return clients


@router.put("/{client_id}", response_model=ClientResponseSchema)
async def update_client(
    client_id: str,
    client_data: ClientCreateSchema,
    service: ClientService = Depends(get_client_service), 
    current_user: User = Depends(get_current_user)
):
    return await service.update_client(client_id, client_data)


@router.delete("/{client_id}")
async def delete_client(
    client_id: str,
    service: ClientService = Depends(get_client_service), 
    current_user: User = Depends(get_current_user)
):
    await service.delete_client(client_id)
    return {"message": "Client deleted"}


# 🔹 Отдельный эндпоинт для загрузки фото
@router.post("/{client_id}/photo", response_model=PhotoUploadResponse)
async def upload_photo(
    client_id: str,
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    service = ClientService(db)
    return await service.upload_client_photo(client_id, photo)


# 🔹 Эндпоинт для получения фото клиента
@router.get("/{client_id}/photo")
async def get_photo(
    client_id: str,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    service = ClientService(db)
    photo_path = await service.get_client_photo(client_id)
    if not os.path.exists(photo_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(photo_path)
