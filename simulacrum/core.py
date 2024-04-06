import math

from simulacrum.models import SimulacrumObject, Vector, SimulacrumState


class SceneEventLoop:
    buffer_size: int = 500
    radius = 200
    current_angle = 0
    angular_speed = math.pi / 500
    rotation_speed = 0.01

    def __init__(self) -> None:
        self.sphere = SimulacrumObject(id=0)
        self.cube = SimulacrumObject(id=1)
        self.calc_coordinates()

    def calc_coordinates(self) -> None:
        x = math.cos(self.current_angle) * self.radius
        y = math.sin(self.current_angle) * self.radius
        self.current_angle += self.angular_speed
        self.sphere.position = Vector(x=x, y=y)
        self.cube.position = Vector(x=-x, y=-y)

    def move_objects(self) -> None:
        self.calc_coordinates()
        rotation = Vector(x=0.01, y=0.01)
        self.sphere.rotation = self.sphere.rotation + rotation
        self.cube.rotation = self.cube.rotation - rotation

    def get_scene(self) -> SimulacrumState:
        return SimulacrumState(objects=[self.sphere, self.cube])
