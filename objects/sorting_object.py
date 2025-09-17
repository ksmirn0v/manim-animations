import copy
from typing import List, Generator, Optional

import numpy as np
from manim import VGroup, RIGHT, DOWN, UP, FadeIn, Succession, AnimationGroup, FadeOut, ScaleInPlace

from config import SortingObjectConfig
from models.animation_holder import AnimationHolder
from models.animation_id import AnimationId
from objects.bar import Bar


class SortingObject(VGroup):

    def __init__(self, bars: List[Bar], config: dict):
        self._config = SortingObjectConfig(**config)
        super().__init__(*bars)
        self.arrange(
            RIGHT,
            buff=self._config.gap_between_bars_local,
            aligned_edge=DOWN,
        ).to_edge(UP, buff=self._config.distance_to_edge_local)

    def get_bar(self, idx: int) -> Bar:
        return self[idx]

    def get_int_numbers(self) -> List[int]:
        return [bar.get_int_number() for bar in list(self)]

    def get_bar_x_coordinates(self) -> List[float]:
        return [float(bar.get_x()) for bar in list(self)]

    def get_fade_in_animation(self, animation_speed: float | None = None) -> Generator[Optional[AnimationHolder], None, None]:

        animations = [FadeIn(item, run_time=animation_speed, shift=DOWN) for item in self]

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_FADE_IN,
            animation=AnimationGroup(*animations, lag_ratio=0.2),
        )

    def get_simple_exchange_animation(
        self,
        bar_left: Bar,
        bar_right: Bar,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        bar_left_pos = bar_left.get_center()
        bar_right_pos = bar_right.get_center()

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_BAR_EXCHANGE,
            animation=Succession(
                AnimationGroup(
                    bar_left.animate.move_to(bar_left_pos + UP * 0.4),
                    bar_right.animate.move_to(bar_right_pos + UP * 0.4),
                    run_time=animation_speed,
                ),
                AnimationGroup(
                    bar_left.animate.move_to(np.array([bar_right_pos[0], bar_left_pos[1], 0])),
                    bar_right.animate.move_to(np.array([bar_left_pos[0], bar_right_pos[1], 0])),
                    run_time=animation_speed,
                )
            ),
        )

    def get_fade_out_animation(self, animation_speed: float | None = None) -> Generator[Optional[AnimationHolder], None, None]:

        animations = [FadeOut(item, run_time=animation_speed, shift=UP) for item in self]

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_FADE_OUT,
            animation=AnimationGroup(*animations, lag_ratio=0.2),
        )

    def get_focus_animation(
        self,
        idx_left: int,
        idx_right: int,
        opacity: float,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        animations = []

        for idx in list(range(idx_left)) + list(range(idx_right+1, len(self))):
            bar = self.get_bar(idx=idx)
            animations.append(next(bar.get_fill_animation(opacity=opacity, animation_speed=animation_speed)).animation)
            animations.append(next(bar.get_stroke_animation(opacity=opacity, animation_speed=animation_speed)).animation)

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_FOCUS,
            animation=AnimationGroup(*animations),
        )

    def get_defocus_animation(
        self,
        idx_left: int,
        idx_right: int,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        animations = []

        for idx in list(range(idx_left)) + list(range(idx_right+1, len(self))):
            bar = self.get_bar(idx=idx)
            animations.append(next(bar.get_fill_animation(opacity=bar._config.fill_opacity, animation_speed=animation_speed)).animation)
            animations.append(next(bar.get_stroke_animation(opacity=bar._config.stroke_opacity, animation_speed=animation_speed)).animation)

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_FOCUS,
            animation=AnimationGroup(*animations),
        )

    def get_select_animation(
        self,
        idx_left: int,
        idx_right: int,
        fill_color: str,
        stroke_color: str | None = None,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        animations = []

        for idx in range(idx_left, idx_right+1):
            bar = self.get_bar(idx=idx)
            animations.append(next(bar.get_fill_animation(color=fill_color, animation_speed=animation_speed)).animation)
            if stroke_color is not None:
                animations.append(next(bar.get_stroke_animation(color=stroke_color, animation_speed=animation_speed)).animation)

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_SELECT,
            animation=AnimationGroup(*animations),
        )

    def get_deselect_animation(
        self,
        idx_left: int,
        idx_right: int,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        animations = []

        for idx in range(idx_left, idx_right+1):
            bar = self.get_bar(idx=idx)
            animations.append(next(bar.get_fill_animation(color=bar._config.fill_color, animation_speed=animation_speed)).animation)
            animations.append(next(bar.get_stroke_animation(color=bar._config.stroke_color, animation_speed=animation_speed)).animation)

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_SELECT,
            animation=AnimationGroup(*animations),
        )

    def get_shift_animation(
        self,
        idx_left: int,
        idx_right: int,
        shift: float,
        animation_speed: float | None = None,
    )-> Generator[Optional[AnimationHolder], None, None]:

        group = self[idx_left:idx_right+1]

        yield AnimationHolder(
            id=AnimationId.SORTING_OBJECT_SHIFT,
            animation=group.animate(run_time=animation_speed).set_y(group.get_y() + shift),
        )

    def get_sort_group_animation(
        self,
        source_indices: list,
        target_indices: list,
        animation_speed: float | None = None,
    ) -> Generator[Optional[AnimationHolder], None, None]:

        if source_indices == target_indices:
            yield None

        source_indices_changed = copy.deepcopy(source_indices)
        source_x_coordinates = self.get_bar_x_coordinates()

        for i in range(len(target_indices)-1):

            source_idx = source_indices[i]
            source_x_coordinate = source_x_coordinates[source_idx]

            target_idx = target_indices[i]
            target_bar = self.get_bar(idx=target_idx)

            if target_idx == source_indices_changed[i]:
                continue

            yield AnimationHolder(
                id=AnimationId.BAR_DISAPPEAR,
                animation=Succession(
                    ScaleInPlace(target_bar, 0.1, run_time=animation_speed),
                    target_bar.animate(run_time=0).set_x(1000.0),
                )
            )

            source_idx_position = source_indices.index(target_idx)
            bars_before_count = target_idx - source_idx
            for j in range(0, bars_before_count):
                bar_before = self.get_bar(idx=source_indices_changed[source_idx_position-j-1])
                yield AnimationHolder(
                    id=AnimationId.BAR_MOVE,
                    animation=bar_before.animate(run_time=animation_speed)
                        .set_x(source_x_coordinates[source_indices[source_idx_position-j]]),
                )
                source_indices_changed[source_idx_position-j] = source_indices_changed[source_idx_position-j-1]
            source_indices_changed[i] = target_idx

            yield AnimationHolder(
                id=AnimationId.BAR_REAPPEAR,
                animation=Succession(
                    AnimationGroup(target_bar.animate(run_time=0).set_x(source_x_coordinate)),
                    AnimationGroup(ScaleInPlace(target_bar, 0.1, run_time=0)),
                    AnimationGroup(ScaleInPlace(target_bar, 10, run_time=animation_speed)),
                )
            )
