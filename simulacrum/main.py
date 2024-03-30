import asyncio

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


cube_id = 0


@app.get("/scene_params")
def scene_params() -> SceneStatement:
    cube = ObjectStatement(id=cube_id)
    return SceneStatement(objects=[cube])


@app.websocket("/scene_changes")
async def scene_changes(websocket: WebSocket):
    await websocket.accept()
    try:
        buffer_size = 500
        rotation = Point()
        while True:
            buffer_request = WebSocketMessage(type=MessageType.request)
            await websocket.send_text(buffer_request.model_dump_json())
            raw_response = await websocket.receive_text()
            response = WebSocketMessage.model_validate_json(raw_response)
            buffer = StatementsBuffer.model_validate_json(response.payload)
            if buffer.length >= buffer_size:
                await asyncio.sleep(0.05)
                continue

            for _ in range(buffer_size):
                rotation = rotation + Vector(x=0.1, y=0.1)
                obj_statement = ObjectStatement(id=cube_id, rotation=rotation)
                statement = SceneStatement(objects=[obj_statement])
                message = WebSocketMessage(
                    type=MessageType.response,
                    payload=statement.model_dump_json()
                )
                await websocket.send_text(message.model_dump_json())

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
