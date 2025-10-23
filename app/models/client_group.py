from sqlalchemy import Column, String, ForeignKey
from .base import Base

class ClientGroup(Base):
    __tablename__ = "client_groups"
    client_id = Column(String, ForeignKey("clients.id"), primary_key=True)
    group_id = Column(String, ForeignKey("groups.id"), primary_key=True)
