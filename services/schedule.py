from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Optional, List

from models.schedule import Schedule
from schemas import ScheduleCreate, Schedule as ScheduleSchema


class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleSchema:
        if not schedule_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")

        db_schedule = Schedule(**schedule_data.model_dump())
        self.db.add(db_schedule)
        await self.db.commit()
        await self.db.refresh(db_schedule)
        return ScheduleSchema.model_validate(db_schedule)

    async def get_schedule(self, schedule_id: str) -> Optional[ScheduleSchema]:
        result = await self.db.execute(select(Schedule).filter(Schedule.id == schedule_id))
        db_schedule = result.scalar_one_or_none()
        if not db_schedule:
            return None
        return ScheduleSchema.model_validate(db_schedule)

    async def list_schedules(self) -> List[ScheduleSchema]:
        result = await self.db.execute(select(Schedule))
        schedules = result.scalars().all()
        return [ScheduleSchema.model_validate(s) for s in schedules]

    async def update_schedule(self, schedule_id: str, schedule_data: ScheduleCreate) -> ScheduleSchema:
        result = await self.db.execute(select(Schedule).filter(Schedule.id == schedule_id))
        db_schedule = result.scalar_one_or_none()
        if not db_schedule:
            raise HTTPException(404, "Schedule not found")

        if not schedule_data.name.strip():
            raise HTTPException(400, "Name cannot be empty")

        for field, value in schedule_data.model_dump().items():
            setattr(db_schedule, field, value)

        await self.db.commit()
        await self.db.refresh(db_schedule)
        return ScheduleSchema.model_validate(db_schedule)

    async def delete_schedule(self, schedule_id: str) -> None:
        result = await self.db.execute(select(Schedule).filter(Schedule.id == schedule_id))
        db_schedule = result.scalar_one_or_none()
        if not db_schedule:
            raise HTTPException(404, "Schedule not found")

        await self.db.delete(db_schedule)
        await self.db.commit()
