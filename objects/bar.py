from typing import Generator, Optional

from manim import VGroup, DOWN, RoundedRectangle, Integer, Succession, AnimationGroup, Wiggle

from config import BarConfig
from models.animation_holder import AnimationHolder
from models.animation_id import AnimationId


class Bar(VGroup):

    def __init__(self, value: int, config: dict):

        self._config = BarConfig(**config)
        rectangle_fill = self._create_rectangle_fill(value=value)
        rectangle_stroke = self._create_rectangle_stroke(value=value)
        rectangle = VGroup(rectangle_fill, rectangle_stroke)
        number = self._create_number(value=value)
        super().__init__(rectangle, number)
        self.arrange(direction=DOWN, buff=self._config.gap_between_rect_and_number_local)

    def _create_rectangle_fill(self, value: int) -> RoundedRectangle:

        rectangle = RoundedRectangle(
            corner_radius=self._config.corner_radius_local,
            width=self._config.width_local,
            height=self._config.height_local * value,
        )
        rectangle.set_fill(color=self._config.fill_color, opacity=self._config.fill_opacity)
        rectangle.z_index = 0
        rectangle.set_stroke(width=0)

        return rectangle

    def _create_rectangle_stroke(self, value: int) -> RoundedRectangle:

        rectangle = RoundedRectangle(
            corner_radius=self._config.corner_radius_local,
            width=self._config.width_local,
            height=self._config.height_local * value,
        )
        rectangle.set_fill(opacity=0.0)
        rectangle.z_index = 1
        rectangle.set_stroke(color=self._config.stroke_color, opacity=self._config.stroke_opacity)

        return rectangle

    def _create_number(self, value: int) -> Integer:

        number = Integer(number=value)
        number.scale(self._config.number_scale_local)

        return number

    def set_default_fill_color(self, color: str):
        self._config.fill_color = color

    def get_default_fill_color(self) -> str:
        return self._config.fill_color

    def get_rectangle(self) -> VGroup:
        return self[0]

    def get_rectangle_fill(self) -> RoundedRectangle:
        return self.get_rectangle()[0]

    def get_rectangle_stroke(self) -> RoundedRectangle:
        return self.get_rectangle()[1]

    def get_number(self) -> Integer:
        return self[1]

    def get_int_number(self) -> int:
        return int(self.get_number().number)

    def get_fill_animation(
        self,
        color: str | None = None,
        opacity: float | None = None,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        if color is None and opacity is None:
            yield None

        yield AnimationHolder(
            id=AnimationId.BAR_FILL,
            animation=self.get_rectangle_fill()
                .animate(run_time=animation_speed)
                .set_fill(color=color, opacity=opacity),
        )

    def get_stroke_animation(
        self,
        color: str | None = None,
        opacity: float | None = None,
        width: float | None = None,
        keep_color: bool = False,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        if color is None and opacity is None and width is None:
            yield None

        if width is None:
            yield AnimationHolder(
                id=AnimationId.BAR_STROKE,
                animation=self.get_rectangle_stroke()
                    .animate(run_time=animation_speed)
                    .set_stroke(color=color, opacity=opacity),
            )
        else:
            last_color = color if keep_color else self._config.stroke_color
            yield AnimationHolder(
                id=AnimationId.BAR_STROKE,
                animation=Succession(
                    AnimationGroup(
                        self.get_rectangle_stroke()
                            .animate
                            .set_stroke(color=color, opacity=opacity, width=width),
                        run_time=animation_speed,
                    ),
                    AnimationGroup(
                        self.get_rectangle_stroke()
                            .animate
                            .set_stroke(color=last_color, width=self._config.stroke_width_px),
                        run_time=animation_speed,
                    )
                ),
            )

    def get_select_animation(
        self,
        fill_color: str | None = None,
        fill_opacity: float | None = None,
        stroke_color: str | None = None,
        stroke_opacity: float | None = None,
        stroke_width: float | None = None,
        keep_color: bool = False,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        if (
            fill_color is None and
            fill_opacity is None and
            stroke_color is None and
            stroke_opacity is None and
            stroke_width is None
        ):
            yield None

        fill_animation = next(
            self.get_fill_animation(color=fill_color, opacity=fill_opacity, animation_speed=animation_speed)
        )
        stroke_animation = next(
            self.get_stroke_animation(color=stroke_color, opacity=stroke_opacity, width=stroke_width, keep_color=keep_color, animation_speed=animation_speed)
        )
        full_animation = [animation_holder.animation for animation_holder in [fill_animation, stroke_animation] if animation_holder is not None]

        if stroke_width is None:
            yield AnimationHolder(
                id=AnimationId.BAR_SELECT,
                animation=AnimationGroup(*full_animation),
            )
        else:
            yield AnimationHolder(
                id=AnimationId.BAR_FOCUS,
                animation=AnimationGroup(*full_animation),
            )

    def get_deselect_animation(
        self,
        fill_color: str | None = None,
        stroke_color: str | None = None,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        if fill_color is None:
            fill_color = self._config.fill_color

        if stroke_color is None:
            stroke_color = self._config.stroke_color

        yield AnimationHolder(
            id=AnimationId.BAR_DESELECT,
            animation=AnimationGroup(
                next(
                    self.get_fill_animation(color=fill_color, opacity=self._config.fill_opacity, animation_speed=animation_speed)
                ).animation,
                next(
                    self.get_stroke_animation(color=stroke_color, opacity=self._config.stroke_opacity, animation_speed=animation_speed)
                ).animation,
            )
        )

    def get_wiggle_animation(
        self,
        angle: float,
        count: int = 3,
        scale: float | None = None,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        obj = self[0]
        if scale is not None:
            obj = self[0].scale(scale_factor=scale)

        yield AnimationHolder(
            id=AnimationId.BAR_WIGGLE,
            animation=Wiggle(
                obj,
                n_wiggles=count,
                rotation_angle=angle,
                run_time=animation_speed,
            )
        )
