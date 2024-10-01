from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from .auth.router import router as auth_router
from .api.calender.router import router as calender_router
from .api.attendance.router import router as attendance_router
from .api.faculties.router import router as faculty_router
from .api.students.router import router as student_router
from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)


app = FastAPI(debug=True, docs_url='/')
app.include_router(auth_router)
app.include_router(calender_router)
app.include_router(attendance_router)
app.include_router(faculty_router)
app.include_router(student_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1:3000',
        'http://localhost:3000',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health-check')
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'working'})