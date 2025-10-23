from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from app.models.room import Room
from app.schemas import RoomCreate, Room as RoomSchema


class RoomService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_room(self, room_data: RoomCreate) -> RoomSchema:
        if not room_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")

        db_room = Room(**room_data.model_dump())
        self.db.add(db_room)
        await self.db.commit()
        await self.db.refresh(db_room)
        return RoomSchema.model_validate(db_room)

    async def get_room(self, room_id: str) -> Optional[RoomSchema]:
        result = await self.db.execute(select(Room).filter(Room.id == room_id))
        db_room = result.scalar_one_or_none()
        if not db_room:
            return None
        return RoomSchema.model_validate(db_room)

    async def list_rooms(self) -> List[RoomSchema]:
        result = await self.db.execute(select(Room))
        rooms = result.scalars().all()
        return [RoomSchema.model_validate(r) for r in rooms]

    async def update_room(self, room_id: str, room_data: RoomCreate) -> RoomSchema:
        result = await self.db.execute(select(Room).filter(Room.id == room_id))
        db_room = result.scalar_one_or_none()
        if not db_room:
            raise HTTPException(404, "Room not found")

        if not room_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")

        db_room.name = room_data.name
        await self.db.commit()
        await self.db.refresh(db_room)
        return RoomSchema.model_validate(db_room)

    async def delete_room(self, room_id: str) -> None:
        result = await self.db.execute(select(Room).filter(Room.id == room_id))
        db_room = result.scalar_one_or_none()
        if not db_room:
            raise HTTPException(404, "Room not found")

        await self.db.delete(db_room)
        await self.db.commit()
