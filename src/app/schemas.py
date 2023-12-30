from pydantic import BaseModel, EmailStr

class AuthCredentials(BaseModel):
    email: EmailStr
    password: str

