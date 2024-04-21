from typing import Any

from pydantic import BaseModel


class WebSocketPayload(BaseModel):
    action: str
    channel: str
    data: Any = None
