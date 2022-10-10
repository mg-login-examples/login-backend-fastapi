from typing import Any
import asyncio

class AsyncStream:
    def __init__(self):
        self._queue = asyncio.Queue()

    async def __aiter__(self):
        try:
            while True:
                yield await self.get()
        except Exception as _:
            pass

    async def get(self) -> Any:
        item = await self._queue.get()
        if item is None:
            raise Exception()
        return item
    
    async def put(self, item: Any):
        await self._queue.put(item)
