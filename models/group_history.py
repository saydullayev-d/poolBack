import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from .base import Base

class GroupHistory(Base):
    __tablename__ = "group_histories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    date = Column(Date, nullable=False)
    action = Column(String, nullable=False)  # 'added' or 'removed', validated in service
    group_id = Column(String, ForeignKey("groups.id"), nullable=False)
