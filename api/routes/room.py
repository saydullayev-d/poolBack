from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.database import get_db
from services.room import RoomService
from schemas import Room, RoomCreate

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=Room)
async def create_room(data: RoomCreate, db: AsyncSession = Depends(get_db)):
    return await RoomService(db).create_room(data)


@router.get("/{room_id}", response_model=Room)
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    room = await RoomService(db).get_room(room_id)
    if not room:
        raise HTTPException(404, "Room not found")
    return room


@router.get("/", response_model=List[Room])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    return await RoomService(db).list_rooms()


@router.put("/{room_id}", response_model=Room)
async def update_room(room_id: str, data: RoomCreate, db: AsyncSession = Depends(get_db)):
    return await RoomService(db).update_room(room_id, data)


@router.delete("/{room_id}")
async def delete_room(room_id: str, db: AsyncSession = Depends(get_db)):
    await RoomService(db).delete_room(room_id)
    return {"message": "Room deleted"}
