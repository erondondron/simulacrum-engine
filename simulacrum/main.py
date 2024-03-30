from datetime import datetime
from time import sleep

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text(f"Сообщение ушло: {datetime.today()}")
        sleep(1)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
