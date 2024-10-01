from fastapi import Depends
from sqlalchemy.orm import Session
from ...models import FacultyMaster
from .schemas import FacultyOutput
from ...utils import get_db

async def fetch_all_faculty(db: Session = Depends(get_db)):
    """Fetch all faculty members."""
    faculty = db.query(FacultyMaster).all()
    return [FacultyOutput.model_validate(faculty.__dict__) for faculty in faculty]