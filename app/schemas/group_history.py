from pydantic import BaseModel, ConfigDict
from datetime import date

class GroupHistorySchema(BaseModel):
    date: date
    action: str  # 'added' or 'removed'
    group_id: str


    model_config = ConfigDict(from_attributes=True)