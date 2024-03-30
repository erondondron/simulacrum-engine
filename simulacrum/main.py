import asyncio
import enum

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

from simulacrum.models import SceneStatement, Point, Vector, ObjectStatement

app = FastAPI()

FPS = 30


class WebSocketCommand(enum.Enum):
    start = "start"
    pause = "pause"


class SceneEventLoop:
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self.state = WebSocketCommand.start

    async def run(self) -> None:
        try:
            await self.websocket.accept()
            await asyncio.gather(
                self.calculate_scene_statements(),
                self.control_buffer_capacity(),
            )
        except WebSocketDisconnect:
            pass

    async def calculate_scene_statements(self) -> None:
        rotation = Point()
        time_step = 0
        while True:
            rotation = rotation + Vector(x=0.1, y=0.1)
            time_step += 1 / FPS
            obj_statement = ObjectStatement(rotation=rotation)
            statement = SceneStatement(objects=[obj_statement])
            await self.websocket.send_text(statement.model_dump_json())

            await asyncio.sleep(0.01)

    async def control_buffer_capacity(self) -> None:
        while True:
            command = await self.websocket.receive_text()
            print(f"Получена команда {command}")
            self.state = WebSocketCommand(command)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await SceneEventLoop(websocket).run()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
