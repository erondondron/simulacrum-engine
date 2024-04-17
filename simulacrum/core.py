from simulacrum.models import SimulacrumObject, NumericVector, SimulacrumState


class SceneEventLoop:
    buffer_size: int = 500
    rotation_speed: float = 0.01
    current_step: float = 0
    step_duration: float = 1 / 60

    def __init__(self, objects: list[SimulacrumObject]) -> None:
        self.objects = objects

    def calc_coordinates(self) -> None:
        # x = parse_expr("0.1").subs("t", 10)
        # y = parse_expr("0.1 * t")
        pass

    def next_step(self) -> None:
        self.current_step += self.step_duration
        self.calc_coordinates()
        rotation = NumericVector(x=0.01, y=0.01)
        for obj in self.objects:
            obj.rotation = obj.rotation + rotation

    def get_scene(self) -> SimulacrumState:
        return SimulacrumState(objects=self.objects)
