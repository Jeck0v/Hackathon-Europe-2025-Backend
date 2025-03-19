from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: str
    username: str
    firstname: str
    name: str
    email: EmailStr
    consent: bool
    role: Optional[str] = "user"

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    firstname: str
    name: str
    email: EmailStr
    password: str
    consent: Optional[bool] = False
    role: Optional[str] = "user"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    consent: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    id: str