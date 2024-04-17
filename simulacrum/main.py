import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulacrum.api import router as projects

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
