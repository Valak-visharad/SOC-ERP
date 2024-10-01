import datetime
import uuid
from datetime import timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .schemas import CalenderInput, CalenderOutput, CalenderUpdate
from ...utils import get_db
from .handler import add_event, delete_val, fetch_all_events, patch_vals
from fastapi.encoders import jsonable_encoder
from ...auth.handler import get_current_user

router = APIRouter(
    prefix='/calender',
    tags=['calender']
)


@router.post('/add-event', response_model=CalenderOutput)
async def create_event(event: CalenderInput, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        res = add_event(event, db, current_user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(res))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})
    

@router.get('/fetch-events', response_model=list[CalenderOutput])
async def fetch_events( db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        events = fetch_all_events(db, current_user)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(events))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})

@router.patch('/update-event', response_model=CalenderOutput)
async def update_event(event: CalenderUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        res = patch_vals(event, db, current_user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(res))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})
    

@router.delete('/delete-event/{event_id}')
async def delete_event(event_id: uuid.UUID, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        res = delete_val(event_id, db, current_user)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})