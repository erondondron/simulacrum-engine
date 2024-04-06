from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from simulacrum.models import Project, SimulacrumState, ProjectState
from simulacrum.settings import STORAGE

PROJECTS_STORAGE = STORAGE.joinpath("projects")
PROJECTS_STORAGE.mkdir(parents=True, exist_ok=True)
PROJECTS_EXTENSION = "smlcrm"

router = APIRouter(prefix="/api")


def get_project_path(uuid: UUID) -> Path:
    file_name = f"{uuid}.{PROJECTS_EXTENSION}"
    return PROJECTS_STORAGE.joinpath(file_name)


def load_project(uuid: UUID) -> ProjectState:
    file = get_project_path(uuid)
    if not file.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectState.model_validate_json(file.read_text())


def dump_project(project: Project) -> None:
    file = get_project_path(project.uid)
    file.write_text(project.model_dump_json())


@router.get("/projects")
async def get_projects() -> list[Project]:
    project_files = PROJECTS_STORAGE.glob(f"*.{PROJECTS_EXTENSION}")
    return [Project.model_validate_json(f.read_text()) for f in project_files]


@router.post("/projects")
async def create_project() -> Project:
    dump_project(new_project := Project())
    return new_project


@router.get("/projects/{project_uuid}")
async def get_project(project_uuid: UUID) -> Project:
    project = load_project(project_uuid)
    project.init_state = SimulacrumState()
    return project


@router.put("/projects/{project_uuid}")
async def update_project(
    project_uuid: UUID,
    project_update: dict[str, Any],
) -> Project:
    project = load_project(project_uuid)
    for key, value in project_update.items():
        setattr(project, key, value)
    dump_project(project)
    return project


@router.delete("/projects/{project_uuid}")
async def delete_project(project_uuid: UUID) -> None:
    file_path = get_project_path(project_uuid)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    file_path.unlink()


@router.get("/projects/{project_uuid}/objects")
async def get_project_objects(project_uuid: UUID) -> SimulacrumState:
    project = load_project(project_uuid)
    return project.init_state


@router.put("/projects/{project_uuid}/objects")
async def update_project_objects(
    project_uuid: UUID,
    project_state: SimulacrumState,
) -> None:
    project = load_project(project_uuid)
    project.init_state = project_state
    dump_project(project)
