import uuid
from sqlalchemy import Column, String
from .base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    position = Column(String, nullable=False)  # trainer | admin | manager
    phone = Column(String, nullable=False)
