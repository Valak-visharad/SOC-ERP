from fastapi import APIRouter, Depends
from typing import List

from requests import Session
from .handler import fetch_all_students
from .schemas import StudentOutput
from ...utils import get_db

router = APIRouter(
    prefix='/students',
    tags=['students']
)

@router.get("/get", response_model=List[StudentOutput])
async def get_students(db: Session = Depends(get_db)):
    return await fetch_all_students(db)