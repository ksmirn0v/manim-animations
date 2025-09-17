import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
import constants
from common.algorithms.sorting_algorithm_scene import SortingAlgorithmScene
from constants import names
from objects.simple_circle import SimpleCircle


class QuickSort(SortingAlgorithmScene):

    def run_initial_animation(self):
        super().run_initial_animation()
        self._swapping_circle = SimpleCircle(config=constants.CONFIG.get_parameters(name=names.SWAPPING_CIRCLE))

    def run_main_animation(self):

        interval_stack = list()
        interval_stack.append((0, len(self._sorting_object.get_int_numbers()) - 1))
        first_iteration = True
        while len(interval_stack) > 0:

            low_idx, high_idx = interval_stack.pop()

            change_needed = False
            for idx in range(low_idx, high_idx):
                if self._sorting_object.get_bar(idx=idx).get_int_number() > self._sorting_object.get_bar(idx=idx + 1).get_int_number():
                    change_needed = True
                    break

            self._animation_manager.select_interval_animation(
                sorting_object=self._sorting_object,
                swapping_circle=self._swapping_circle,
                idx_left=low_idx,
                idx_right=high_idx,
                first_iteration=first_iteration,
                change_needed=change_needed,
            )

            if not change_needed:
                self._animation_manager.wiggle_bars_animation(
                    sorting_object=self._sorting_object,
                    indices=list(range(low_idx, high_idx + 1))
                )
                self._animation_manager.deselect_interval_animation(
                    sorting_object=self._sorting_object,
                    swapping_circle=self._swapping_circle,
                    idx_left=low_idx,
                    idx_right=high_idx,
                    first_iteration=first_iteration,
                    change_needed=change_needed,
                )
                continue

            swapping_idx = low_idx
            pivot_idx = high_idx

            pivot_bar = self._sorting_object.get_bar(idx=pivot_idx)

            for moving_idx in range(low_idx, high_idx):
                moving_bar = self._sorting_object.get_bar(idx=moving_idx)
                self._animation_manager.select_bar_animation(
                    bar=moving_bar,
                    is_lower=moving_bar.get_int_number() <= pivot_bar.get_int_number(),
                )
                if moving_bar.get_int_number() <= pivot_bar.get_int_number():
                    if moving_idx > swapping_idx:
                        self._animation_manager.exchange_bars_animation(sorting_object=self._sorting_object, idx_left=swapping_idx, idx_right=moving_idx)
                        self._sorting_object[moving_idx], self._sorting_object[swapping_idx] = self._sorting_object[swapping_idx], self._sorting_object[moving_idx]
                    swapping_idx += 1
                    self._animation_manager.move_swapping_circle_animation(
                        swapping_circle=self._swapping_circle,
                        sorting_object=self._sorting_object,
                        new_idx=swapping_idx,
                        low_idx=low_idx,
                    )
                self._animation_manager.deselect_bar_animation(bar=moving_bar)

            self._animation_manager.select_bar_animation(
                bar=pivot_bar,
                swapping_circle=self._swapping_circle,
            )
            self._animation_manager.exchange_bars_animation(sorting_object=self._sorting_object, idx_left=swapping_idx, idx_right=pivot_idx)
            self._sorting_object[swapping_idx], self._sorting_object[pivot_idx] = self._sorting_object[pivot_idx], self._sorting_object[swapping_idx]
            self._animation_manager.deselect_interval_animation(
                sorting_object=self._sorting_object,
                swapping_circle=self._swapping_circle,
                idx_left=low_idx,
                idx_right=high_idx,
                first_iteration=first_iteration,
                change_needed=change_needed,
            )

            if low_idx < swapping_idx-1:
                interval_stack.append((low_idx, swapping_idx-1))
            if swapping_idx+1 < high_idx:
                interval_stack.append((swapping_idx+1, high_idx))

            first_iteration = False

        self.wait(0.5)
        self._animation_manager.color_left_over_bars_animation(sorting_object=self._sorting_object)
        self.wait(0.5)
