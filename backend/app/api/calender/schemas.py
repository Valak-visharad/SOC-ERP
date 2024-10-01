import datetime
import uuid
from pydantic import BaseModel

class CalenderInput(BaseModel):
    date: datetime.date
    event: str

    class config:
        from_attributes = True

class CalenderOutput(BaseModel):
    id: uuid.UUID
    date: datetime.date
    event: str
    user_id: uuid.UUID

class CalenderUpdate(BaseModel):
    id: uuid.UUID
    event: str