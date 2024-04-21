from pydantic import BaseModel, EmailStr


class UserPasswordReset(BaseModel):
    email: EmailStr
    password: str
    token: str
