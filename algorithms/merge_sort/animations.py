from typing import List

from manim import Scene, AnimationGroup, Succession

from models.animation_id import AnimationId
from objects.sorting_object import SortingObject


class AnimationManager:

    def _set_constants(self, config: dict):

        self._ANIMATION_SPEED = config.get('ANIMATION_SPEED', 0.5)
        self._ANIMATION_SPEED_FADE_IN = config.get('ANIMATION_SPEED_FADE_IN', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_FADE_OUT = config.get('ANIMATION_SPEED_FADE_OUT', self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_BAR_WIGGLE = config.get("ANIMATION_SPEED_BAR_WIGGLE", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_FOCUS = config.get("ANIMATION_SPEED_SORTING_OBJECT_FOCUS", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_SELECT = config.get("ANIMATION_SPEED_SORTING_OBJECT_SELECT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_SHIFT = config.get("ANIMATION_SPEED_SORTING_OBJECT_SHIFT", self._ANIMATION_SPEED)
        self._ANIMATION_SPEED_SORTING_OBJECT_SORT_GROUP = config.get("ANIMATION_SPEED_SORTING_OBJECT_SORT_GROUP", self._ANIMATION_SPEED)
        self._SORTING_OBJECT_FOCUS_OPACITY = config.get("SORTING_OBJECT_FOCUS_OPACITY")
        self._SORTING_OBJECT_SELECT_FILL_COLOR_LEFT = config.get("SORTING_OBJECT_SELECT_FILL_COLOR_LEFT")
        self._SORTING_OBJECT_SELECT_FILL_COLOR_RIGHT = config.get("SORTING_OBJECT_SELECT_FILL_COLOR_RIGHT")
        self._SORTING_OBJECT_SHIFT = config.get("SORTING_OBJECT_SHIFT")
        self._BAR_SELECT_FILL_COLOR = config.get("BAR_SELECT_FILL_COLOR")
        self._BAR_SELECT_FILL_OPACITY = config.get("BAR_SELECT_FILL_OPACITY")
        self._BAR_SELECT_MIN_STROKE_OPACITY = config.get("BAR_SELECT_MIN_STROKE_OPACITY")
        self._BAR_SELECT_MIN_STROKE_WIDTH = config.get("BAR_SELECT_MIN_STROKE_WIDTH")
        self._BAR_WIGGLE_COUNT = config.get("BAR_WIGGLE_COUNT")
        self._BAR_WIGGLE_ANGLE = config.get("BAR_WIGGLE_ANGLE")
        self._BAR_WIGGLE_SCALE = config.get("BAR_WIGGLE_SCALE")

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
        idx_left_start: int,
        idx_left_end: int,
        idx_right_start: int,
        idx_right_end: int,
    ):

        animation = AnimationGroup(
            next(
                sorting_object.get_focus_animation(
                    idx_left=idx_left_start,
                    idx_right=idx_right_end,
                    opacity=self._SORTING_OBJECT_FOCUS_OPACITY,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_FOCUS),
            ).animation,
            next(
                sorting_object.get_select_animation(
                    idx_left=idx_left_start,
                    idx_right=idx_left_end,
                    fill_color=self._SORTING_OBJECT_SELECT_FILL_COLOR_LEFT,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SELECT,
                )
            ).animation,
            next(
                sorting_object.get_select_animation(
                    idx_left=idx_right_start,
                    idx_right=idx_right_end,
                    fill_color=self._SORTING_OBJECT_SELECT_FILL_COLOR_RIGHT,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SELECT,
                )
            ).animation,
        )

        self._scene.add_sound("media/sfx/merge_sort/bars_highlight.mp3", gain=-15)
        self._scene.play(animation)

        animation = AnimationGroup(
            next(
                sorting_object.get_shift_animation(
                    idx_left=idx_left_start,
                    idx_right=idx_right_end,
                    shift=self._SORTING_OBJECT_SHIFT,
                    animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SHIFT,
                )
            ).animation,
        )

        self._scene.play(animation)


    def sort_two_groups_animation(
        self,
        sorting_object: SortingObject,
        source_indices: List[int],
        target_indices: List[int],
    ):

        animations = sorting_object.get_sort_group_animation(
            source_indices=source_indices,
            target_indices=target_indices,
            animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SORT_GROUP,
        )

        for animation in animations:

            if animation is None:

                self._scene.add_sound("media/sfx/merge_sort/bar_wiggle.mp3", gain=-19)
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
                            ).animation for idx in source_indices
                        ],
                    )
                )
                continue

            if animation.id == AnimationId.BAR_DISAPPEAR:
                self._scene.add_sound("media/sfx/merge_sort/bar_disappear.mp3", gain=-5)
            if animation.id == AnimationId.BAR_MOVE:
                self._scene.add_sound("media/sfx/merge_sort/bar_move.mp3", gain=-15)
            if animation.id == AnimationId.BAR_REAPPEAR:
                self._scene.add_sound("media/sfx/merge_sort/bar_appear.mp3", gain=-10)
            self._scene.play(animation.animation)

    def deselect_interval_animation(
        self,
        sorting_object: SortingObject,
        idx_left: int,
        idx_right: int,
    ):

        animation = next(
            sorting_object.get_shift_animation(
                idx_left=idx_left,
                idx_right=idx_right,
                shift=-self._SORTING_OBJECT_SHIFT,
                animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SHIFT,
            )
        ).animation
        self._scene.play(animation)

        animation = next(
            sorting_object.get_defocus_animation(
                idx_left=idx_left,
                idx_right=idx_right,
                animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_FOCUS
            )
        ).animation
        self._scene.play(animation)

        animation = next(
            sorting_object.get_deselect_animation(
                idx_left=idx_left,
                idx_right=idx_right,
                animation_speed=self._ANIMATION_SPEED_SORTING_OBJECT_SELECT,
            )
        ).animation
        self._scene.play(animation)
