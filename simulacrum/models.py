from __future__ import annotations

import enum
from typing import Self
from uuid import UUID, uuid4

from pydantic import Field, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SimulacrumModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class WSMessageType(enum.StrEnum):
    """Тип сообщения веб сокета"""
    request = "request"
    response = "response"


class WebSocketMessage(SimulacrumModel):
    """
    Сообщение веб сокета

    :param type: Тип сообщения веб сокета
    :param payload: Полезная нагрузка сообщения в формате json
    """
    type: WSMessageType
    payload: str | None = None


class GUIBuffer(SimulacrumModel):
    """
    Информация о буфере состояний

    :param length: Текущая длина буфера
    """
    length: int


class Project(SimulacrumModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str = "NewProject"


class Vector(SimulacrumModel):
    x: float = 0
    y: float = 0
    z: float = 0

    # TODO(erondondron): Вынести в core?
    def __add__(self, other: Vector) -> Self:
        return Vector(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    # TODO(erondondron): Вынести в core?
    def __sub__(self, other: Vector) -> Self:
        return Vector(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )


class ObjectType(enum.StrEnum):
    sphere = "sphere"
    cube = "cube"


class SimulacrumObject(SimulacrumModel):
    """
    Объект симулякра

    :param id: Уникальный идентификатор
    :param type: Тип объекта
    :param position: Координаты в пространстве
    :param rotation: Поворот объекта
    """

    id: int
    type: ObjectType

    position: Vector = Field(default_factory=Vector)
    rotation: Vector = Field(default_factory=Vector)


class SimulacrumState(SimulacrumModel):
    objects: list[SimulacrumObject] = Field(default_factory=list)


class ProjectState(Project):
    init_state: SimulacrumState = Field(default_factory=SimulacrumState)
