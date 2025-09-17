import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.algorithms.sorting_algorithm_scene import SortingAlgorithmScene


class BubbleSort(SortingAlgorithmScene):

    def run_main_animation(self):

        # --- Main bubble sort animation ---
        value_count = len(self._sorting_object.get_int_numbers())
        for i in range(value_count):

            for j in range(1, value_count-i):

                bar_left = self._sorting_object.get_bar(idx=j-1)
                bar_right = self._sorting_object.get_bar(idx=j)

                if bar_left.get_int_number() > bar_right.get_int_number():
                    self._animation_manager.select_bars_animation(bar_left=bar_left, bar_right=bar_right)
                    self._animation_manager.exchange_bars_animation(sorting_object=self._sorting_object, idx_left=j-1, idx_right=j)
                    self._sorting_object[j-1], self._sorting_object[j] = self._sorting_object[j], self._sorting_object[j-1]
                    self._animation_manager.deselect_bars_animation(bar_left=bar_left, bar_right=bar_right)
                else:
                    self._animation_manager.select_bars_animation(bar_left=bar_left, bar_right=bar_right, is_left_bigger=False)
                    self._animation_manager.wiggle_bars_animation(bar_left=bar_left, bar_right=bar_right)
                    self._animation_manager.deselect_bars_animation(bar_left=bar_left, bar_right=bar_right)

            # Mark i as fixed
            bar_final = self._sorting_object.get_bar(idx=value_count-1-i)
            self._animation_manager.set_final_bar_animation(bar=bar_final)
