from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import date


# 👇 Подсхема для описания посещаемости конкретного клиента
class AttendanceRecord(BaseModel):
    present: bool
    reason: Optional[str] = None


# 👇 Базовая схема расписания
class ScheduleBase(BaseModel):
    name: str
    room_id: str
    type: str  # group | individual | special
    trainer_id: str
    group_id: Optional[str] = None
    date: date
    start_time: str
    end_time: str

    # ✅ массив дней недели
    days_of_week: Optional[List[str]] = Field(default_factory=list)

    # ✅ список ID клиентов
    client_ids: Optional[List[str]] = Field(default_factory=list)

    # ✅ словарь посещаемости
    attendance: Optional[Dict[str, AttendanceRecord]] = Field(default_factory=dict)

    # ✅ проведено ли занятие
    conducted: bool = False


# 👇 Для создания новой записи
class ScheduleCreate(ScheduleBase):
    pass


# 👇 Для обновления существующей записи
class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    room_id: Optional[str] = None
    type: Optional[str] = None
    trainer_id: Optional[str] = None
    group_id: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    days_of_week: Optional[List[str]] = None
    client_ids: Optional[List[str]] = None
    attendance: Optional[Dict[str, AttendanceRecord]] = None
    conducted: Optional[bool] = None


# 👇 Для чтения данных (GET)
class ScheduleRead(ScheduleBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
