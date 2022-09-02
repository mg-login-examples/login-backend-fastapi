from pydantic import BaseModel, EmailStr

class UserPasswordChange(BaseModel):
    username: EmailStr
    password: str
    password_new: str
