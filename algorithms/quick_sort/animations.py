from typing import List, Optional

from manim import Scene, AnimationGroup, Circle, FadeOut

from objects.bar import Bar
from objects.simple_circle import SimpleCircle
from objects.sorting_object import SortingObject


class AnimationManager:

    def _set_constants(self, config: dict):

        self._ANIMATION_SPEED = config.get('ANIMATION_SPEED', 0.5)
        self._ANIMATION_SPEED_FADE_IN = config.get('ANIMATION_SPEED_FADE_IN', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_FADE_OUT = config.get('ANIMATION_SPEED_FADE_OUT', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_SELECT = config.get("ANIMATION_SPEED_BAR_SELECT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_EXCHANGE = config.get('ANIMATION_SPEED_BAR_EXCHANGE', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_WIGGLE = config.get("ANIMATION_SPEED_BAR_WIGGLE", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_FOCUS = config.get("ANIMATION_SPEED_SORTING_OBJECT_FOCUS", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_SELECT = config.get("ANIMATION_SPEED_SORTING_OBJECT_SELECT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_SHIFT = config.get("ANIMATION_SPEED_SORTING_OBJECT_SHIFT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_CIRCLE_FADE_IN = config.get("ANIMATION_SPEED_CIRCLE_FADE_IN", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_CIRCLE_FADE_OUT = config.get("ANIMATION_SPEED_CIRCLE_FADE_OUT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_CIRCLE_SELECT = config.get("ANIMATION_SPEED_CIRCLE_SELECT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_CIRCLE_MOVE = config.get("ANIMATION_SPEED_CIRCLE_MOVE", self._ANIMATION_SPEED)
        self._SORTING_OBJECT_FOCUS_OPACITY = config.get("SORTING_OBJECT_FOCUS_OPACITY")
        self._SORTING_OBJECT_SHIFT = config.get("SORTING_OBJECT_SHIFT")
        self._BAR_SELECT_LOWER_FILL_COLOR = config.get("BAR_SELECT_LOWER_FILL_COLOR")
        self._BAR_SELECT_HIGHER_FILL_COLOR = config.get("BAR_SELECT_HIGHER_FILL_COLOR")
        self._BAR_SELECT_FINAL_FILL_COLOR = config.get("BAR_SELECT_FINAL_FILL_COLOR")
        self._BAR_PIVOT_FILL_COLOR = config.get("BAR_PIVOT_FILL_COLOR")
        self._BAR_SELECT_STROKE_WIDTH = config.get("BAR_SELECT_STROKE_WIDTH")
        self._BAR_WIGGLE_COUNT = config.get("BAR_WIGGLE_COUNT")
        self._BAR_WIGGLE_ANGLE = config.get("BAR_WIGGLE_ANGLE")
        self._BAR_WIGGLE_SCALE = config.get("BAR_WIGGLE_SCALE")
        self._CIRCLE_SELECT_STROKE_WIDTH = config.get("CIRCLE_SELECT_STROKE_WIDTH")

    def __init__(self, scene: Scene, config: dict):
        self._scene = scene
        self._set_constants(config=config)

    def fade_in_animation(self, sorting_object: SortingObject):

        animation = next(
            sorting_object.get_fade_in_animation(animation_speed=self._ANIMATION_SPEED_FADE_IN)
        ).animation

        self._scene.play(animation)

    def fade_out_animation(self, sorting_object: SortingObject):

        animation = next(
            sorting_object.get_fade_out_animation(animation_speed=self._ANIMATION_SPEED_FADE_OUT)
        ).animation

        self._scene.play(animation)


    def select_interval_animation(
        self,
        sorting_object: SortingObject,
        swapping_circle: SimpleCircle,
        idx_left: int,
        idx_right: int,
        first_iteration: bool,
        change_needed: bool
    ):

        animation = AnimationGroup(
            next(
                sorting_object.get_shift_animation(
                    idx_left=idx_left,
                    idx_right=idx_right,
                    shift=0.0 if first_iteration else self._SORTING_OBJECT_SHIFT,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SHIFT,
                )
            ).animation,
            next(
                sorting_object.get_focus_animation(
                    idx_left=idx_left,
                    idx_right=idx_right,
                    opacity=None if first_iteration else self._SORTING_OBJECT_FOCUS_OPACITY,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_FOCUS),
            ).animation,
        )

        if not first_iteration:
            self._scene.add_sound("media/sfx/quick_sort/bar_move.mp3", gain=-18, time_offset=-0.3)
        self._scene.play(animation)

        swapping_circle.set_stroke_color(color=self._BAR_PIVOT_FILL_COLOR)
        swapping_circle.set_position(
            x=sorting_object.get_bar(idx=idx_left).get_number().get_x(),
            y=sorting_object.get_bar(idx=idx_left).get_number().get_y(),
        )

        if change_needed:
            animation = AnimationGroup(
                next(
                    sorting_object.get_bar(idx=idx_right).get_select_animation(
                        fill_color=self._BAR_PIVOT_FILL_COLOR,
                        stroke_width=self._BAR_SELECT_STROKE_WIDTH,
                        animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SELECT,
                    )
                ).animation,
                next(
                    swapping_circle.get_fade_in_animation(
                        animation_speed=self._ANIMATION_SPEED_CIRCLE_FADE_IN,
                    )
                ).animation,
            )

            self._scene.add_sound("media/sfx/quick_sort/bar_initial_select.mp3", gain=-23)
            self._scene.play(animation)

    def select_bar_animation(self, bar: Bar, swapping_circle: Optional[SimpleCircle] = None, is_lower: Optional[bool] = None):

        if is_lower is None:
            fill_color = self._BAR_SELECT_FINAL_FILL_COLOR
        elif is_lower:
            fill_color = self._BAR_SELECT_LOWER_FILL_COLOR
        else:
            fill_color = self._BAR_SELECT_HIGHER_FILL_COLOR

        animations = [
            next(
                bar.get_select_animation(
                    fill_color=fill_color,
                    stroke_width=self._BAR_SELECT_STROKE_WIDTH,
                    animation_speed=self._ANIMATION_SPEED_BAR_SELECT,
                )
            ).animation
        ]

        if swapping_circle is not None:
            swapping_circle.set_stroke_color(color=self._BAR_SELECT_FINAL_FILL_COLOR)
            animations.append(
                next(
                    swapping_circle.get_select_animation(
                        stroke_width=self._CIRCLE_SELECT_STROKE_WIDTH,
                        animation_speed=self._ANIMATION_SPEED_CIRCLE_SELECT,
                    )
                ).animation
            )

        self._scene.add_sound("media/sfx/quick_sort/bar_select.mp3", gain=-35)
        self._scene.play(AnimationGroup(*animations))

    def deselect_bar_animation(self, bar: Bar):

        animation = next(
            bar.get_deselect_animation(animation_speed=self._ANIMATION_SPEED_BAR_SELECT),
        ).animation

        self._scene.play(animation)

    def exchange_bars_animation(self, sorting_object: SortingObject, idx_left: int, idx_right: int):

        bar_left = sorting_object.get_bar(idx=idx_left)
        bar_right = sorting_object.get_bar(idx=idx_right)

        animation = next(
            sorting_object.get_simple_exchange_animation(
                bar_left=bar_left,
                bar_right=bar_right,
                animation_speed=self._ANIMATION_SPEED_BAR_EXCHANGE,
            )
        ).animation

        self._scene.add_sound("media/sfx/quick_sort/bar_exchange.mp3", gain=-23)
        self._scene.play(animation)

    def move_swapping_circle_animation(self, swapping_circle: SimpleCircle, sorting_object: SortingObject, new_idx: int, low_idx: int):

        if new_idx != low_idx:
            animation = next(
                swapping_circle.get_move_animation(
                    x=sorting_object.get_bar(idx=new_idx).get_number().get_x(),
                    animation_speed=self._ANIMATION_SPEED_CIRCLE_MOVE,
                )
            ).animation
            self._scene.add_sound("media/sfx/quick_sort/circle_move.mp3", gain=-35)
            self._scene.play(animation)

    def wiggle_bars_animation(self, sorting_object: SortingObject, indices: List[int]):

        self._scene.add_sound("media/sfx/quick_sort/bar_wiggle.mp3", gain=-24, time_offset=0.2)
        self._scene.play(
            AnimationGroup(
                *[
                    next(
                        sorting_object.get_bar(idx=idx).get_wiggle_animation(
                            angle=self._BAR_WIGGLE_ANGLE,
                            count=self._BAR_WIGGLE_COUNT,
                            scale=self._BAR_WIGGLE_SCALE,
                            animation_speed=self._ANIMATION_SPEED_BAR_WIGGLE,
                        )
                    ).animation for idx in indices
                ],
            )
        )

    def deselect_interval_animation(
        self,
        sorting_object: SortingObject,
        swapping_circle: SimpleCircle,
        idx_left: int,
        idx_right: int,
        first_iteration: bool,
        change_needed: bool,
    ):

        animations = [
            next(
                sorting_object.get_shift_animation(
                    idx_left=idx_left,
                    idx_right=idx_right,
                    shift=0.0 if first_iteration else -self._SORTING_OBJECT_SHIFT,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SHIFT,
                )
            ).animation,
        ]
        if change_needed:
            animations.append(FadeOut(swapping_circle, run_time=self._ANIMATION_SPEED))
        self._scene.play(AnimationGroup(*animations))

        animation = next(
            sorting_object.get_defocus_animation(
                idx_left=idx_left,
                idx_right=idx_right,
                animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_FOCUS
            )
        ).animation
        self._scene.play(animation)

    def color_left_over_bars_animation(self, sorting_object: SortingObject):

        bars = [sorting_object.get_bar(idx=idx) for idx in range(len(sorting_object))]
        not_colored_bars = [bar for bar in bars if bar.get_rectangle_fill().fill_color.get_hex() != self._BAR_SELECT_FINAL_FILL_COLOR.lower()]

        animations = [
            next(
                bar.get_select_animation(
                    fill_color=self._BAR_SELECT_FINAL_FILL_COLOR,
                    stroke_width=self._BAR_SELECT_STROKE_WIDTH,
                    animation_speed=self._ANIMATION_SPEED_BAR_SELECT,
                )
            ).animation
            for bar in not_colored_bars
        ]

        self._scene.play(AnimationGroup(*animations, lag_ratio=0.1))


