from __future__ import annotations

import uuid as uid
from typing import Self

from pydantic import BaseModel as PydanticModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModel(PydanticModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Point(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0

    def __add__(self, other: Point) -> Self:
        return Point(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )


class Vector(Point):
    ...


class CameraStatement(BaseModel):
    """
    Камера сцены

    :param field_of_view: Угол обзора
    :param position: Координаты размещения камеры
    """
    field_of_view: float = 75
    position: Point


class ObjectStatement(BaseModel):
    """
    Состояние объекта

    :param uuid: Уникальный идентификатор
    :param time: Время с начала запуска [мс]
    :param coordinates: Координаты в пространстве
    :param rotation: Поворот объекта
    """

    uuid: uid.UUID = Field(default_factory=uid.uuid4)
    time: float = 0

    coordinates: Point = Field(default_factory=Point)
    rotation: Point = Field(default_factory=Point)


class SceneStatement(BaseModel):
    camera: CameraStatement | None = None
    objects: list[ObjectStatement] = Field(default_factory=list)
