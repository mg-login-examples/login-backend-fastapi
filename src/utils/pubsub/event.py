from typing import Any

from pydantic import BaseModel

class Event(BaseModel):
    channel: str
    message: Any = None
