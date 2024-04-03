from fastapi import APIRouter

from simulacrum.models.project import Project
from simulacrum.settings import STORAGE

PROJECTS_STORAGE = STORAGE.joinpath("projects")
PROJECTS_STORAGE.mkdir(parents=True, exist_ok=True)
PROJECTS_EXTENSION = "smlcrm"

router = APIRouter()


@router.get("/projects")
async def get_projects() -> list[Project]:
    project_files = PROJECTS_STORAGE.glob(f"*.{PROJECTS_EXTENSION}")
    return [Project.model_validate_json(f.read_text()) for f in project_files]


@router.post("/projects")
async def create_project() -> Project:
    new_project = Project()
    file_name = f"{new_project.uid}.{PROJECTS_EXTENSION}"
    file_path = PROJECTS_STORAGE.joinpath(file_name)
    file_path.write_text(new_project.model_dump_json())
    return new_project
