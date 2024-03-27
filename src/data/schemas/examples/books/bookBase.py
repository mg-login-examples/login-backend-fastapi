from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    number_of_pages: Optional[int] = None
