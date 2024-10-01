import datetime
import uuid
from pydantic import BaseModel

class StudentOutput(BaseModel):
    id: uuid.UUID
    roll_number: str
    enrollment_number: str
    name: str
    department: str
    email: str
    year: int
    admission_year: int
    course_name: str
    specialization: str
    division: str
    age: int
    phone: str
    blood_group: str
    secondary_phone: str
    gender: str
    dob: datetime.date
    guardian_type: str
    guardian_name: str
    guardian_phone: str