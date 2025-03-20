from pydantic import BaseModel
from typing import Optional

class DEMOCompromiseResponse(BaseModel):
    id_subject: str
    text: str

    class Config:
        from_attributes = True

class DEMOCompromiseCreate(BaseModel):
    id_subject: str
    text: str

class DEMOCompromiseUpdate(BaseModel):
    id_subject: Optional[str] = None
    text: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    id: str