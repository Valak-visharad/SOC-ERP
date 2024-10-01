from fastapi import APIRouter, Depends
from requests import Session
from .handler import fetch_all_faculty
from .schemas import FacultyOutput
from ...utils import get_db

router = APIRouter(
    prefix='/faculty',
    tags=['faculty']
)

@router.get("/get", response_model=list[FacultyOutput])
async def get_faculty(db: Session = Depends(get_db)):
    return await fetch_all_faculty(db)