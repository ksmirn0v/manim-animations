import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.algorithms.sorting_algorithm_scene import SortingAlgorithmScene


class SelectionSort(SortingAlgorithmScene):

    def run_main_animation(self):

        # --- Main selection sort animation ---
        value_count = len(self._sorting_object.get_int_numbers())
        for bar_idx in range(value_count):

            min_idx = bar_idx
            bar_current_min = self._sorting_object.get_bar(idx=min_idx)
            self._animation_manager.set_min_bar_animation(bar=bar_current_min)

            for j in range(bar_idx + 1, value_count):

                bar_candidate = self._sorting_object.get_bar(idx=j)
                self._animation_manager.select_bar_animation(bar=bar_candidate)

                if bar_candidate.get_int_number() >= bar_current_min.get_int_number():
                    self._animation_manager.deselect_bar_animation(bar=bar_candidate)
                else:
                    self._animation_manager.refocus_min_bar_animation(min_bar=bar_current_min, other_bar=bar_candidate)
                    bar_current_min = bar_candidate
                    min_idx = j

            # After scanning, if min changed, swap i and min_idx
            if min_idx != bar_idx:

                self._animation_manager.exchange_bars_animation(sorting_object=self._sorting_object, idx_left=bar_idx, idx_right=min_idx)
                # Update logical structures
                self._sorting_object[bar_idx], self._sorting_object[min_idx] = self._sorting_object[min_idx], self._sorting_object[bar_idx]

            # Mark i as fixed
            bar_final = self._sorting_object.get_bar(idx=bar_idx)
            self._animation_manager.set_final_bar_animation(bar=bar_final)
