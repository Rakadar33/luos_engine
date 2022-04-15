from typing import List
import queue
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


async def myfunc():
    for i in range(app.queue_limit):
        if not app.queue_system.empty():
            obj = app.queue_system.get_nowait()
            if obj['websocket'] in manager.active_connections:
                await manager.send_personal_message(f"You wrote: {obj['message']}", obj['websocket'])

manager = ConnectionManager()

aquaApp = FastAPI()
aquaApp.queue_system = queue.Queue()
aquaApp.queue_limit = 5

app.scheduler = AsyncIOScheduler()
app.scheduler.add_job(myfunc, 'interval', seconds=5)
app.scheduler.start()


@aquaApp.get("/")
async def root():
    doc= "Test bot\n"\
         +"doc"
    return {"message": doc}
