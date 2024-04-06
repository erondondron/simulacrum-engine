import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from simulacrum.api import router as projects
from simulacrum.core import SceneEventLoop
from simulacrum.models import WSMessageType, WebSocketMessage, GUIBuffer

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


@app.websocket("/scene_changes")
async def scene_changes(websocket: WebSocket):
    await websocket.accept()
    try:
        scene = SceneEventLoop()
        while True:
            buffer_request = WebSocketMessage(type=WSMessageType.request)
            await websocket.send_text(buffer_request.model_dump_json())
            raw_response = await websocket.receive_text()
            response = WebSocketMessage.model_validate_json(raw_response)
            buffer = GUIBuffer.model_validate_json(response.payload)
            if buffer.length >= scene.buffer_size:
                await asyncio.sleep(0.05)
                continue

            for _ in range(scene.buffer_size):
                scene.move_objects()
                message = WebSocketMessage(
                    type=WSMessageType.response,
                    payload=scene.get_scene().model_dump_json()
                )
                await websocket.send_text(message.model_dump_json())

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
