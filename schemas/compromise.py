from pydantic import BaseModel
from typing import Optional

class DataCompromiseResponse(BaseModel):
    id_subject: str
    id_user: str
    text: str

    class Config:
        from_attributes = True

class DataCompromiseCreate(BaseModel):
    id_subject: str
    id_user: str
    text: str

class DataCompromiseUpdate(BaseModel):
    id_subject: Optional[str] = None
    id_user: Optional[str] = None
    text: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str