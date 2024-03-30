from __future__ import annotations

import enum
from typing import Self

from pydantic import BaseModel as PydanticModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModel(PydanticModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class MessageType(enum.StrEnum):
    """
    Тип сообщения веб сокета

    :param request: Запрос информации
    :param response: Предоставление информации
    """
    request = "request"
    response = "response"


class WebSocketMessage(BaseModel):
    """
    Сообщение веб сокета

    :param type: Тип сообщения веб сокета
    :param payload: Полезная нагрузка сообщения в формате json
    """
    type: MessageType
    payload: str | None = None


class StatementsBuffer(BaseModel):
    """
    Информация о буфере состояний сцены

    :param length: Текущая длина буфера
    """
    length: int


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

    :param id: Уникальный идентификатор
    :param coordinates: Координаты в пространстве
    :param rotation: Поворот объекта
    """

    id: int
    coordinates: Point = Field(default_factory=Point)
    rotation: Point = Field(default_factory=Point)


class SceneStatement(BaseModel):
    """
    Состояние сцены

    :param camera: Изменение состояния камеры
    :param objects: Изменение состояний объектов
    """

    camera: CameraStatement | None = None
    objects: list[ObjectStatement] = Field(default_factory=list)
