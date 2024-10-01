import uuid
from pydantic import BaseModel

class FacultyOutput(BaseModel):
    id: uuid.UUID
    name: str
    qualification: str
    department: str
    email: str
    age: int
    phone: str