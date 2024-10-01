import uuid
from .schemas import CalenderInput, CalenderOutput, CalenderUpdate
from ...utils import get_db
from ...models import Calendar, UserMaster, UserRole
from ...auth.handler import get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import or_



def add_event(event: CalenderInput, db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):   
    
    db_event = Calendar(**event.model_dump())
    db_event.user_id = current_user.id
    db_event.id = uuid.uuid4()
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def fetch_all_events(db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):

    events = db.query(Calendar).join(UserMaster).filter(
        or_(
            UserMaster.role == UserRole.SUPER_ADMIN,
            Calendar.user_id == current_user.id
        )
    ).all()
    
    return [CalenderOutput.model_validate(event.__dict__) for event in events]

def patch_vals(new_event: CalenderUpdate, db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):

    event = db.query(Calendar).filter(Calendar.id == new_event.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    event.event = new_event.event
    db.commit()
    db.refresh(event)
    return event


def delete_val(event_id: uuid.UUID, db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):
    
    event = db.query(Calendar).filter(Calendar.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    db.delete(event)
    db.commit()