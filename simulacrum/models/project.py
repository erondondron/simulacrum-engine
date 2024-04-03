from uuid import UUID, uuid4

from pydantic import Field

from simulacrum.models.base import SimulacrumModel


class Project(SimulacrumModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str = "NewProject"
