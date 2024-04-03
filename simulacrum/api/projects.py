from fastapi import APIRouter

from simulacrum.models.project import Project

router = APIRouter()


@router.post("/projects")
async def create_project() -> Project:
    return Project()
