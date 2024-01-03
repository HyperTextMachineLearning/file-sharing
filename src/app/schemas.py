from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserIn(UserBase):
    password: str

class UserInDBBase(UserBase):
    class Config:
        orm_mode = True

class UserInDB(UserInDBBase):
    hashed_password: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class File(BaseModel):
    file_name: str
    class Config:
        orm_mode = True