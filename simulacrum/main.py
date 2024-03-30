import asyncio
import math

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from simulacrum.models import SceneStatement, Point, Vector, ObjectStatement, \
    WebSocketMessage, MessageType, StatementsBuffer

app = FastAPI()

# FIXME(erondondron): Костыль для обхода ошибок CORS
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SceneEventLoop:
    buffer_size: int = 500
    radius = 1.5
    angular_speed = math.pi / 100
    rotation_speed = 0.01

    def __init__(self) -> None:
        self.cube_0 = ObjectStatement(id=0, coordinates=Point(y=self.radius))
        self.cube_1 = ObjectStatement(id=1, coordinates=Point(y=-self.radius))

    def move_objects(self) -> None:
        rotation = Vector(x=0.01, y=0.01)
        self.cube_0.rotation = self.cube_0.rotation + rotation
        self.cube_1.rotation = self.cube_1.rotation - rotation

    def get_scene(self) -> SceneStatement:
        return SceneStatement(objects=[self.cube_0, self.cube_1])


@app.get("/scene_params")
def scene_params() -> SceneStatement:
    return SceneEventLoop().get_scene()


@app.websocket("/scene_changes")
async def scene_changes(websocket: WebSocket):
    await websocket.accept()
    try:
        scene = SceneEventLoop()
        while True:
            buffer_request = WebSocketMessage(type=MessageType.request)
            await websocket.send_text(buffer_request.model_dump_json())
            raw_response = await websocket.receive_text()
            response = WebSocketMessage.model_validate_json(raw_response)
            buffer = StatementsBuffer.model_validate_json(response.payload)
            if buffer.length >= scene.buffer_size:
                await asyncio.sleep(0.05)
                continue

            for _ in range(scene.buffer_size):
                scene.move_objects()
                message = WebSocketMessage(
                    type=MessageType.response,
                    payload=scene.get_scene().model_dump_json()
                )
                await websocket.send_text(message.model_dump_json())

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
