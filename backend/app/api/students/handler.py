from fastapi import Depends
from sqlalchemy.orm import Session
from ...models import StudentMaster
from .schemas import StudentOutput
from ...utils import get_db

async def fetch_all_students(db: Session = Depends(get_db)):
    """Fetch all students."""
    students = db.query(StudentMaster).all()
    return [StudentOutput.model_validate(student.__dict__) for student in students]