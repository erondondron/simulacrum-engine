import asyncio
import math

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from simulacrum.api.projects import router as projects
from simulacrum.models.scene import SceneStatement, Point, Vector, ObjectStatement, \
    WebSocketMessage, MessageType, StatementsBuffer

app = FastAPI()

app.include_router(projects)

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
    radius = 200
    current_angle = 0
    angular_speed = math.pi / 500
    rotation_speed = 0.01

    def __init__(self) -> None:
        self.sphere = ObjectStatement(id=0)
        self.cube = ObjectStatement(id=1)
        self.calc_coordinates()

    def calc_coordinates(self) -> None:
        x = math.cos(self.current_angle) * self.radius
        y = math.sin(self.current_angle) * self.radius
        self.current_angle += self.angular_speed
        self.sphere.coordinates = Point(x=x, y=y)
        self.cube.coordinates = Point(x=-x, y=-y)

    def move_objects(self) -> None:
        self.calc_coordinates()
        rotation = Vector(x=0.01, y=0.01)
        self.sphere.rotation = self.sphere.rotation + rotation
        self.cube.rotation = self.cube.rotation - rotation

    def get_scene(self) -> SceneStatement:
        return SceneStatement(objects=[self.sphere, self.cube])


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
