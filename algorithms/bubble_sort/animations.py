from manim import Scene, AnimationGroup

from objects.bar import Bar
from objects.sorting_object import SortingObject


class AnimationManager:

    def _set_constants(self, config: dict):

        self._ANIMATION_SPEED = config.get('ANIMATION_SPEED', 0.5)
        self._ANIMATION_SPEED_FADE_IN = config.get('ANIMATION_SPEED_FADE_IN', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_FADE_OUT = config.get('ANIMATION_SPEED_FADE_OUT', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_SELECT = config.get('ANIMATION_SPEED_BAR_SELECT', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_DESELECT = config.get("ANIMATION_SPEED_BAR_DESELECT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_EXCHANGE = config.get("ANIMATION_SPEED_BAR_EXCHANGE", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_FINAL_SELECT = config.get("ANIMATION_SPEED_BAR_FINAL_SELECT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_WIGGLE = config.get("ANIMATION_SPEED_BAR_WIGGLE", self._ANIMATION_SPEED)
        self._BAR_SELECT_FILL_COLOR = config.get("BAR_SELECT_FILL_COLOR")
        self._BAR_SELECT_FILL_OPACITY = config.get("BAR_SELECT_FILL_OPACITY")
        self._BAR_SELECT_MIN_STROKE_OPACITY = config.get("BAR_SELECT_MIN_STROKE_OPACITY")
        self._BAR_SELECT_MIN_STROKE_WIDTH = config.get("BAR_SELECT_MIN_STROKE_WIDTH")
        self._BAR_SELECT_FINAL_FILL_COLOR = config.get("BAR_SELECT_FINAL_FILL_COLOR")
        self._BAR_SELECT_FINAL_FILL_OPACITY = config.get("BAR_SELECT_FINAL_FILL_OPACITY", self._BAR_SELECT_FILL_OPACITY)
        self._BAR_SELECT_FINAL_STROKE_COLOR = config.get("BAR_SELECT_FINAL_STROKE_COLOR")
        self._BAR_SELECT_FINAL_STROKE_OPACITY = config.get("BAR_SELECT_FINAL_STROKE_OPACITY", self._BAR_SELECT_MIN_STROKE_OPACITY)
        self._BAR_SELECT_FINAL_STROKE_WIDTH = config.get("BAR_SELECT_FINAL_STROKE_WIDTH", self._BAR_SELECT_MIN_STROKE_WIDTH)
        self._BAR_WIGGLE_COUNT = config.get("BAR_WIGGLE_COUNT")
        self._BAR_WIGGLE_ANGLE = config.get("BAR_WIGGLE_ANGLE")

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


    def select_bars_animation(self, bar_left: Bar, bar_right: Bar, is_left_bigger: bool = True):

        if is_left_bigger:
            animation = AnimationGroup(
                next(
                    bar_left.get_select_animation(
                        fill_color=self._BAR_SELECT_FILL_COLOR,
                        fill_opacity=self._BAR_SELECT_FILL_OPACITY,
                        animation_speed=self._ANIMATION_SPEED_BAR_SELECT,
                    )
                ).animation,
                next(
                    bar_right.get_select_animation(
                        fill_color=self._BAR_SELECT_FILL_COLOR,
                        fill_opacity=self._BAR_SELECT_FILL_OPACITY,
                        stroke_width=self._BAR_SELECT_MIN_STROKE_WIDTH,
                        animation_speed=self._ANIMATION_SPEED_BAR_SELECT,
                    )
                ).animation,
            )
        else:
            animation = AnimationGroup(
                next(
                    bar_left.get_select_animation(
                        fill_color=self._BAR_SELECT_FILL_COLOR,
                        fill_opacity=self._BAR_SELECT_FILL_OPACITY,
                        stroke_width=self._BAR_SELECT_MIN_STROKE_WIDTH,
                        animation_speed=self._ANIMATION_SPEED_BAR_SELECT,
                    )
                ).animation,
                next(
                    bar_right.get_select_animation(
                        fill_color=self._BAR_SELECT_FILL_COLOR,
                        fill_opacity=self._BAR_SELECT_FILL_OPACITY,
                        animation_speed=self._ANIMATION_SPEED_BAR_SELECT,
                    )
                ).animation,
            )

        self._scene.add_sound("media/sfx/bubble_sort/bar_select.mp3", gain=-2, time_offset=0.1)
        self._scene.play(animation)


    def deselect_bars_animation(self, bar_left: Bar, bar_right: Bar):

        animation = AnimationGroup(
            next(
                bar_left.get_deselect_animation(animation_speed=self._ANIMATION_SPEED_BAR_DESELECT)
            ).animation,
            next(
                bar_right.get_deselect_animation(animation_speed=self._ANIMATION_SPEED_BAR_DESELECT)
            ).animation,
        )

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

        self._scene.add_sound("media/sfx/bubble_sort/bar_exchange.mp3", gain=-21)
        self._scene.play(animation)

    def wiggle_bars_animation(self, bar_left: Bar, bar_right: Bar):

        animation = AnimationGroup(
            next(
                bar_left.get_wiggle_animation(
                    angle=self._BAR_WIGGLE_ANGLE,
                    count=self._BAR_WIGGLE_COUNT,
                    animation_speed=self._ANIMATION_SPEED_BAR_WIGGLE,
                )
            ).animation,
            next(
                bar_right.get_wiggle_animation(
                    angle=self._BAR_WIGGLE_ANGLE,
                    count=self._BAR_WIGGLE_COUNT,
                    animation_speed=self._ANIMATION_SPEED_BAR_WIGGLE,
                )
            ).animation,
        )

        self._scene.add_sound("media/sfx/bubble_sort/bar_wiggle.mp3", gain=-20, time_offset=0.2)
        self._scene.play(animation)

    def set_final_bar_animation(self, bar: Bar):

        animation = next(
            bar.get_select_animation(
                fill_color=self._BAR_SELECT_FINAL_FILL_COLOR,
                fill_opacity=self._BAR_SELECT_FINAL_FILL_OPACITY,
                stroke_color=self._BAR_SELECT_FINAL_STROKE_COLOR,
                stroke_opacity=self._BAR_SELECT_FINAL_STROKE_OPACITY,
                stroke_width=self._BAR_SELECT_FINAL_STROKE_WIDTH,
                animation_speed=self._ANIMATION_SPEED_BAR_FINAL_SELECT,
            )
        ).animation

        self._scene.add_sound("media/sfx/bubble_sort/bar_fixed.mp3", gain=-9)
        self._scene.play(animation)
