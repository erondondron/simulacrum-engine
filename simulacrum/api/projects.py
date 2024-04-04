from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from simulacrum.models.project import Project
from simulacrum.settings import STORAGE

PROJECTS_STORAGE = STORAGE.joinpath("projects")
PROJECTS_STORAGE.mkdir(parents=True, exist_ok=True)
PROJECTS_EXTENSION = "smlcrm"

router = APIRouter()


def get_project_path(uuid: UUID) -> Path:
    file_name = f"{uuid}.{PROJECTS_EXTENSION}"
    return PROJECTS_STORAGE.joinpath(file_name)


@router.get("/projects")
async def get_projects() -> list[Project]:
    project_files = PROJECTS_STORAGE.glob(f"*.{PROJECTS_EXTENSION}")
    return [Project.model_validate_json(f.read_text()) for f in project_files]


@router.post("/projects")
async def create_project() -> Project:
    new_project = Project()
    file_path = get_project_path(new_project.uid)
    file_path.write_text(new_project.model_dump_json())
    return new_project


@router.get("/projects/{project_uuid}")
async def get_project(project_uuid: UUID) -> Project:
    file_path = get_project_path(project_uuid)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    return Project.model_validate_json(file_path.read_text())


@router.put("/projects/{project_uuid}")
async def update_project(
    project_uuid: UUID,
    project_update: dict[str, Any],
) -> Project:
    project = await get_project(project_uuid)
    for key, value in project_update.items():
        setattr(project, key, value)
    file_path = get_project_path(project_uuid)
    file_path.write_text(project.model_dump_json())
    return project


@router.delete("/projects/{project_uuid}")
async def delete_project(project_uuid: UUID) -> None:
    file_path = get_project_path(project_uuid)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    file_path.unlink()
