from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

class ScheduleBase(BaseModel):
    name: str
    room_id: str
    type: str  # "group" | "individual" | "special"
    trainer: str  # Employee.name
    group: Optional[str] = None
    client_ids: List[str] = []
    date: date
    start_time: str  # HH:MM
    end_time: str    # HH:MM
    attendance: Optional[Dict[str, str]] = None
    days_of_week: List[str] = []

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: str

    class Config:
        from_attributes = True
