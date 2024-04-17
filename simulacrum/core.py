from sympy import parse_expr

from simulacrum.models import SimulacrumObject, NumericVector, SimulacrumState


class SceneEventLoop:
    buffer_size: int = 500
    rotation_speed: float = 0.01
    current_step: float = 0
    step_duration: float = 1 / 60

    def __init__(self, objects: list[SimulacrumObject]) -> None:
        self.objects = objects

    def calc_coordinates(self) -> None:
        for obj in self.objects:
            x = parse_expr(obj.motion_equation.x or "0")
            y = parse_expr(obj.motion_equation.y or "0")
            prev_step = self.current_step - self.step_duration
            dx = x.subs("t", self.current_step) - x.subs("t", prev_step)
            dy = y.subs("t", self.current_step) - y.subs("t", prev_step)
            obj.position.x = obj.position.x + dx
            obj.position.y = obj.position.y + dy

    def next_step(self) -> None:
        self.current_step += self.step_duration
        self.calc_coordinates()
        rotation = NumericVector(x=0.01, y=0.01)
        for obj in self.objects:
            obj.rotation = obj.rotation + rotation

    def get_scene(self) -> SimulacrumState:
        return SimulacrumState(objects=self.objects)
