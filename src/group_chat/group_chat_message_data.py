from typing import Any
from pydantic import BaseModel


class GroupChatMessageData(BaseModel):
    text: str
