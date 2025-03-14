from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: str
    username: str
    firstname: str
    name: str
    email: EmailStr
    role: Optional[str] = "user"

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
