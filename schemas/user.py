from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id_user: str
    username: str
    firstname: str
    name: str
    age: int
    gender: str
    country: str
    email: EmailStr
    consent: Optional[bool] = False
    identity_verif: Optional[bool] = False
    role: Optional[str] = "user"
    historic: list
    streak: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    id_user: str
    username: str
    firstname: str
    name: str
    age: int
    gender: str
    country: str
    email: EmailStr
    password: str
    consent: Optional[bool] = False
    identity_verif: Optional[bool] = False
    role: Optional[str] = "user"
    historic: list
    streak: int

class UserUpdate(BaseModel):
    id_user: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    consent: Optional[bool] = False
    identity_verif: Optional[bool] = False
    role: Optional[str] = "user"
    historic: Optional[list] = None
    streak: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    id_user: str