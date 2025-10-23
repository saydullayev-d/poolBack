from sqlalchemy import Column, String, Date, ForeignKey, JSON, Boolean
import uuid
from sqlalchemy.orm import relationship
from .base import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=False)
    type = Column(String, nullable=False)  # group | individual | special
    trainer_id = Column(String, ForeignKey("employees.id"), nullable=False)
    group_id = Column(String, ForeignKey("groups.id"), nullable=True)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

    # ✅ новые JSON-поля
    client_ids = Column(JSON, nullable=True)
    attendance = Column(JSON, nullable=True)
    days_of_week = Column(JSON, nullable=True)  # теперь массив (list)

    # ✅ новое поле
    conducted = Column(Boolean, default=False)
