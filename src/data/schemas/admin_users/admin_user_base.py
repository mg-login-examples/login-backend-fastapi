from pydantic import BaseModel, EmailStr

class AdminUserBase(BaseModel):
    email: EmailStr
