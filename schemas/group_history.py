from pydantic import BaseModel
from datetime import date

class GroupHistorySchema(BaseModel):
    date: date
    action: str  # 'added' or 'removed'
    group_id: str
