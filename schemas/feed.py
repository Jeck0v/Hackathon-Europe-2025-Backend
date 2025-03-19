from pydantic import BaseModel
from typing import List, Dict, Optional

class FeedResponse(BaseModel):
    id_subject: str
    short_description: str
    image: str
    context: str
    impact: List[str]
    source: str
    votes: Dict[str, int]  

    class Config:
        from_attributes = True

class FeedCreate(BaseModel):
    id_subject: str
    short_description: str
    image: str
    context: str
    impact: List[str] 
    source: str
    votes: Dict[str, int]  

class FeedUpdate(BaseModel):
    id_subject: Optional[str] = None
    short_description: Optional[str] = None
    image: Optional[str] = None
    context: Optional[str] = None
    impact: Optional[List[str]] = None 
    source: Optional[str] = None
    votes: Optional[Dict[str, int]] = None 

class Token(BaseModel):
    access_token: str
    token_type: str