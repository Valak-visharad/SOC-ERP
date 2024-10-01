import datetime
import uuid
from datetime import timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .schemas import BulkRegistrationResponse, ResetPassword, UserCreate, Token, UserLogin, UserResponse
from .handler import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash, get_current_user, get_user
from ..utils import get_db
from ..models import UserMaster, UserRole
import pandas as pd
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from jose import JWTError, jwt

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
RESET_PASSWORD_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


# conf = ConnectionConfig(
#     MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
#     MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
#     MAIL_FROM=os.getenv("MAIL_FROM"),
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True
# )

def create_reset_password_token(email: str):
    expire = datetime.datetime.now(UTC) + timedelta(minutes=RESET_PASSWORD_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, user.email)
    if existing_user:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "Username already registered"})
    hashed_password = get_password_hash(user.password)
    new_user = UserMaster(
        id=uuid.uuid4(),
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login', response_model=Token)
async def login_for_access_token(user_login: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response.set_cookie(key="access_token",
                        value=access_token, httponly=True, samesite='none', secure=True)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/users/me', response_model=UserResponse)
async def read_users_me(current_user: UserMaster = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {'detail': 'Logged out successfully'}

@router.post('/register/single', response_model=UserResponse)
async def register_single_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Only superadmin can register users")
    
    existing_user = get_user(db, user.email)
    if existing_user:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "Username already registered"})
    
    new_user = UserMaster(
        id=uuid.uuid4(),
        email=user.email,
        password=get_password_hash(str(uuid.uuid4())),
        role=user.role
    )
    if new_user:
        
        reset_token = create_reset_password_token(new_user.email)
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        
        try:
            # Setup email
            msg = MIMEMultipart()
            msg['From'] = os.getenv('MAIL_USERNAME')
            msg['To'] = new_user.email
            msg['Subject'] = "Password Reset"
            
            body = f"""<!DOCTYPE html>
    <html lang=\"en\">
    <head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Password Reset</title>
    <style>
      *,html{{
        margin:0;
        padding:0;
        box-sizing:border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      }}
      .container {{
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background:#f7f7f7;
        border:0.5px solid #6481992e;;
      }}
      h1 {{
        text-align: center;
        color: #333333;
        margin-bottom: 20px;
      }}
      p {{
        color: #666666;
        line-height: 1.6;
        margin-bottom: 20px;
      }}
      .reset-button {{
        display: inline-block;
        padding: 10px 20px;
        margin-bottom: 15px;
        background-color: #4CAF50;
        color: #ffffff !important; 
        text-decoration: none ;
        border-radius: 5px;
        transition: background-color 0.3s;
      }}
      .reset-button:hover {{
        background-color: #45a049;
      }}
    </style>
    </head>
    <body>
      <div class=\"container\">
        <h1>Password Reset</h1>
        <p>Greetings, <br>
            Welcome to SOC-Portal
            </p>
        <p>
            To start using your account, you have to change your password for the first time.
            Use the button below to change your password </p>
        <div align= \"center\">
        <a href=\"{reset_link}"  class=\"reset-button\">Reset Password</a>      
        </div>
        <p>If you did not request an account creation on SOC-Portal, you can safely ignore this email.</p>
        <p>Thanks,<br>SOC-Portal</p>
      </div>
    </body>
    </html>
    """
            msg.attach(MIMEText(body, 'html'))

            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtpserver:
                smtpserver.ehlo()
                smtpserver.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                smtpserver.send_message(msg)

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
        
    return new_user

@router.post('/register/bulk', response_model=BulkRegistrationResponse)
async def register_bulk_users(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserMaster = Depends(get_current_user)):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Only superadmin can register users")
    
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")

    df = pd.read_excel(file.file)
    registered_users = []
    failed_users = []
    
    for _, row in df.iterrows():
        user = UserCreate(email=row['email'], role=row['role'])
        
        existing_user = get_user(db, user.email)
        if existing_user:
            failed_users.append({'email': user.email, 'reason': 'User already registered'})
            continue  

        new_user = UserMaster(
            id=uuid.uuid4(),
            email=user.email,
            password=get_password_hash(str(uuid.uuid4())),
            role=user.role
        )
        if new_user:
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                
                reset_token = create_reset_password_token(new_user.email)
                reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        
                msg = MIMEMultipart()
                msg['From'] = os.getenv('MAIL_USERNAME')
                msg['To'] = new_user.email
                msg['Subject'] = "Password Reset"
                
                body = f"""<!DOCTYPE html>
                        <html lang=\"en\">
                        <head>
                        <meta charset=\"UTF-8\">
                        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
                        <title>Password Reset</title>
                        <style>
                        *,html{{
                            margin:0;
                            padding:0;
                            box-sizing:border-box;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 20px auto;
                            padding: 20px;
                            background:#f7f7f7;
                            border:0.5px solid #6481992e;;
                        }}
                        h1 {{
                            text-align: center;
                            color: #333333;
                            margin-bottom: 20px;
                        }}
                        p {{
                            color: #666666;
                            line-height: 1.6;
                            margin-bottom: 20px;
                        }}
                        .reset-button {{
                            display: inline-block;
                            padding: 10px 20px;
                            margin-bottom: 15px;
                            background-color: #4CAF50;
                            color: #ffffff !important; 
                            text-decoration: none ;
                            border-radius: 5px;
                            transition: background-color 0.3s;
                        }}
                        .reset-button:hover {{
                            background-color: #45a049;
                        }}
                        </style>
                        </head>
                        <body>
                        <div class=\"container\">
                            <h1>Password Reset</h1>
                            <p>Greetings, <br>
                                Welcome to SOC-Portal
                                </p>
                            <p>
                                To start using your account, you have to change your password for the first time.
                                Use the button below to change your password </p>
                            <div align= \"center\">
                            <a href=\"{reset_link}"  class=\"reset-button\">Reset Password</a>      
                            </div>
                            <p>If you did not request an account creation on SOC-Portal, you can safely ignore this email.</p>
                            <p>Thanks,<br>SOC-Portal</p>
                        </div>
                        </body>
                        </html>
                        """
                msg.attach(MIMEText(body, 'html'))

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtpserver:
                    smtpserver.ehlo()
                    smtpserver.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                    smtpserver.send_message(msg)

                registered_users.append(new_user)
            except Exception as e:
                db.rollback()
                failed_users.append({'email': user.email, 'reason': f"Failed to register user and send email: {str(e)}"})
        else:
            failed_users.append({'email': user.email, 'reason': 'Failed to create user'})
    
    return BulkRegistrationResponse(
        registered_users=[UserResponse(id=user.id, email=user.email, role=user.role) for user in registered_users],
        failed_users=failed_users
    )

@router.post('/reset-password')
async def reset_password(reset_password: ResetPassword, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(reset_password.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = get_user(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password = get_password_hash(reset_password.new_password)
    db.commit()
    db.refresh(user)
    
    return {"detail": "Password reset successful"}