from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
