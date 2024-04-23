from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    number_of_pages: int | None = None
