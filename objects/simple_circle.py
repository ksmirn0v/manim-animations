from typing import Generator, Optional

from manim import VGroup, Circle, FadeIn, Succession, AnimationGroup, FadeOut

from config import SimpleCircleConfig
from models.animation_holder import AnimationHolder
from models.animation_id import AnimationId


class SimpleCircle(VGroup):

    def __init__(self, config: dict):

        self._config = SimpleCircleConfig(**config)
        circle = self._create_circle()
        super().__init__(circle)

    def _create_circle(self) -> Circle:

        circle = Circle(radius=self._config.radius_local)

        return circle

    def set_stroke_color(self, color: str):

        self[0].set_color(color=color)

    def set_position(self, x: float, y: float):

        self[0].set_x(x)
        self[0].set_y(y)

    def get_fade_in_animation(self, animation_speed: float | None = None) -> Generator[Optional[AnimationHolder], None, None]:

        animation = FadeIn(self, run_time=animation_speed)

        yield AnimationHolder(
            id=AnimationId.CIRCLE_FADE_IN,
            animation=animation
        )

    def get_select_animation(self, stroke_width: float,  animation_speed: float | None = None) -> Generator[Optional[AnimationHolder], None, None]:

        animation = Succession(
            AnimationGroup(self[0].animate(run_time=animation_speed).set(stroke_width=stroke_width)),
            AnimationGroup(self[0].animate(run_time=animation_speed).set(stroke_width=self._config.stroke_width_px)),
        )

        yield AnimationHolder(
            id=AnimationId.CIRCLE_SELECT,
            animation=animation
        )

    def get_move_animation(self, x: float, animation_speed: float | None = None) -> Generator[Optional[AnimationHolder], None, None]:

        animation = self.animate(run_time=animation_speed).set_x(x)

        yield AnimationHolder(
            id=AnimationId.CIRCLE_MOVE,
            animation=animation
        )

    def get_fade_out_animation(self, animation_speed: float | None = None) -> Generator[Optional[AnimationHolder], None, None]:

        animation = FadeOut(self, run_time=animation_speed)

        yield AnimationHolder(
            id=AnimationId.CIRCLE_FADE_OUT,
            animation=animation
        )
