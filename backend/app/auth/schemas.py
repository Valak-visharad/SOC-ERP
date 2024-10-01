from uuid import UUID
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    email: str
    role: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    role: str

class BulkRegistrationResponse(BaseModel):
    registered_users: list[UserResponse]
    failed_users: list[dict[str, str]]

    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str

    
class TokenData(BaseModel):
    email: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str

class ResetPassword(BaseModel):
    token: str
    new_password: str
