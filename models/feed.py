from pydantic import BaseModel
from typing import List, Dict, Optional

class DataFeed(BaseModel):
    id_subject: str
    short_description: str
    image: str
    context: str
    impact: List
    source: str
    votes: Dict[str, int] = {"0": 0, "1": 0, "2": 0}

class DataFeedResponse(BaseModel):
    id_subject: str
    short_description: str
    image: str
    context: str
    impact: List
    source: str
    votes: Dict[str, int] = {"0": 0, "1": 0, "2": 0}

    class Config:
        orm_mode = True

class DataFeedUpdate(BaseModel):
    id_subject: Optional[str] = None
    short_description: Optional[str] = None
    image: Optional[str] = None
    context: Optional[str] = None
    impact: Optional[List[str]] = None
    source: Optional[str] = None
    votes: Optional[Dict[str, int]] = None