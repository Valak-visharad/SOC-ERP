import os

from fastapi import Depends
from requests import Session
from ...models import AttendanceMaster, FacultyMaster, UserMaster
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path
from ...utils import get_db
from ...auth.handler import get_current_user

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

PARENT = Path(__file__).resolve().parent

# Paths for credentials and token files
CREDENTIALS_PATH = PARENT / 'credentials.json'
TOKEN_PATH = PARENT / "./token.json"

def get_credentials():
    """Get and refresh user credentials for Google Sheets API."""
    credentials = None
    if os.path.exists(TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(credentials.to_json())
    
    return credentials

def read_values(spreadsheet_id, range_name):
    """Read values from a specified range in the Google Sheet."""
    try:
        service = build("sheets", "v4", credentials=get_credentials())
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        sheetdata = result.get("values", [])
        maxsizeoflist = max(len(row) for row in sheetdata) if sheetdata else 0
        return {"values": sheetdata, "max_size": maxsizeoflist}  # Return as a dictionary
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def write_values(spreadsheet_id, range_name, values):
    """Write values to a specified range in the Google Sheet."""
    try:
        service = build("sheets", "v4", credentials=get_credentials())
        body = {"values": values}
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def append_values(spreadsheet_id, range_name, values):
    """Append values to a specified range in the Google Sheet."""
    try:
        service = build("sheets", "v4", credentials=get_credentials())
        body = {"values": values}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def batch_update(spreadsheet_id, requests):
    """Execute a batch update on the Google Sheet."""
    try:    
        service = build("sheets", "v4", credentials=get_credentials())
        body = {"requests": requests}
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def getfacultyclasses(faculty_id):
    try:
        facultyclasses = []
        
        return facultyclasses
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def fetch_faculty_class_list(db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):
    """Get list of classes for a faculty."""
    faculty_id = db.query(FacultyMaster).filter_by(user_id=current_user.id).first().id
    classes = db.query(AttendanceMaster).filter_by(faculty_id=faculty_id).all()
    return classes