from pydantic import BaseModel
from typing import Optional

class CompromiseResponse(BaseModel):
    id_subject: str
    id_user: str
    text: str

    class Config:
        from_attributes = True

class CompromiseCreate(BaseModel):
    id_subject: str
    id_user: str
    text: str

class CompromiseUpdate(BaseModel):
    id_subject: Optional[str] = None
    id_user: Optional[str] = None
    text: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str