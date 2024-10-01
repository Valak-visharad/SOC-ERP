from fastapi import APIRouter, Depends, HTTPException
from typing import Any

from requests import Session
from .handler import read_values, write_values, append_values, batch_update, fetch_faculty_class_list
from ...utils import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ...models import UserMaster
from ...auth.handler import get_current_user

router = APIRouter(
    prefix='/attendance',
    tags=['attendance']
)

@router.get('/read/{spreadsheet_id}/{range_name}', response_model=dict[str, Any])
async def read_values_endpoint(spreadsheet_id: str, range_name: str):
    """Read values from a specified range in the Google Sheet."""
    values = read_values(spreadsheet_id, range_name)
    if values is None:
        raise HTTPException(status_code=500, detail="Failed to read values from the spreadsheet.")
    return values

@router.post('/write/{spreadsheet_id}/{range_name}', response_model=dict[str, Any])
async def write_values_endpoint(spreadsheet_id: str, range_name: str, values: list[list[str]]):
    """Write values to a specified range in the Google Sheet."""
    result = write_values(spreadsheet_id, range_name, values)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to write values to the spreadsheet.")
    return result

@router.post('/append/{spreadsheet_id}/{range_name}', response_model=dict[str, Any])
async def append_values_endpoint(spreadsheet_id: str, range_name: str, values: list[list[str]]):
    """Append values to a specified range in the Google Sheet."""
    result = append_values(spreadsheet_id, range_name, values)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to append values to the spreadsheet.")
    return result

@router.post('/batch-update/{spreadsheet_id}', response_model=dict[str, Any])
async def batch_update_endpoint(spreadsheet_id: str, requests: list[dict[str, Any]]):
    """Execute a batch update on the Google Sheet."""
    response = batch_update(spreadsheet_id, requests)
    if response is None:
        raise HTTPException(status_code=500, detail="Failed to perform batch update on the spreadsheet.")
    return response

@router.get('/faculty-class-list', response_model=Any)
async def get_faculty_class_list(db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):
    """Get the list of classes taught by the faculty."""
    try:
        res = fetch_faculty_class_list(db, current_user)
        return JSONResponse(status_code=200, content=jsonable_encoder(res))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))