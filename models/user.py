from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    firstname: str
    name: str
    email: EmailStr
    password: str
    consent: Optional[bool] = False
    role: Optional[str] = "user"

class UserResponse(BaseModel):
    id: str
    username: str
    firstname: str
    name: str
    email: EmailStr
    consent: bool
    role: Optional[str] = "user"
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    consent: Optional[bool] = None
class UserInDB(User):
    hashed_password: str

