from abc import ABC, abstractmethod
from typing import Any

from ..event import Event


class PubSubBackendAbstract(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def ping(self) -> None:
        pass

    @abstractmethod
    async def publish(self, channel: str, message: str) -> None:
        pass

    @abstractmethod
    async def subscribe(self, channel: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        pass

    @abstractmethod
    async def get_next_event(self) -> Event:
        pass
