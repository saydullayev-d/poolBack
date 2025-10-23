from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.auth import get_current_user
from app.models import User
from app.models.database import get_db
from app.services.schedule import ScheduleService
from app.schemas import Schedule, ScheduleCreate

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.post("/", response_model=Schedule)
async def create_schedule(data: ScheduleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ScheduleService(db).create_schedule(data)


@router.get("/{schedule_id}", response_model=Schedule)
async def get_schedule(schedule_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedule = await ScheduleService(db).get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(404, "Schedule not found")
    return schedule


@router.get("/", response_model=List[Schedule])
async def list_schedules(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ScheduleService(db).list_schedules()


@router.put("/{schedule_id}", response_model=Schedule)
async def update_schedule(schedule_id: str, data: ScheduleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ScheduleService(db).update_schedule(schedule_id, data)


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await ScheduleService(db).delete_schedule(schedule_id)
    return {"message": "Schedule deleted"}
