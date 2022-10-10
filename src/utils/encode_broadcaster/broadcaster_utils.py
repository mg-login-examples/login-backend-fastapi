from fastapi import FastAPI
from broadcaster import Broadcast

def add_broadcaster(app: FastAPI, broadcast_url: str):

    broadcast = Broadcast(broadcast_url)

    @app.on_event("startup")
    async def startup_event():
        await broadcast.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await broadcast.disconnect()

    return broadcast
