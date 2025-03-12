from pydantic import BaseModel

class UserCreate(BaseModel):
    firstname: str
    name: str
    email: str
    password: str

class UserInResponse(BaseModel):
    firstname: str
    name: str
    email: str
    _id: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
