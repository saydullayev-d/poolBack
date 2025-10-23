from pydantic import BaseModel, ConfigDict

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
