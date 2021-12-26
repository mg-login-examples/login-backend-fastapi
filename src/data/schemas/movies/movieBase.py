from typing import Optional

from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    summary: Optional[str] = None
    duration: Optional[int] = None
