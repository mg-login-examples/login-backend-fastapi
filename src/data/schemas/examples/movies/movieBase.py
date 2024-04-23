from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    summary: str | None = None
    duration: int | None = None
