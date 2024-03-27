from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
