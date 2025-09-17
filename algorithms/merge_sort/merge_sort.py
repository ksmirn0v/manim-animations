import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.algorithms.sorting_algorithm_scene import SortingAlgorithmScene


class MergeSort(SortingAlgorithmScene):

    def run_main_animation(self):

        # define split intervals
        index_split = dict()
        self.split(d=index_split, left_idx=0, right_idx=len(self._bars)-1, level=0)

        # animate
        for level in range(len(index_split) - 1, -1, -1):
            for interval in index_split[level]:
                self._animation_manager.select_interval_animation(
                    sorting_object=self._sorting_object,
                    idx_left_start=interval["left"][0],
                    idx_left_end=interval["left"][1],
                    idx_right_start=interval["right"][0],
                    idx_right_end=interval["right"][1],
                )
                arr = self._sorting_object.get_int_numbers()
                target_indices = MergeSort.merge(
                    arr=arr,
                    left_start_idx=interval["left"][0],
                    left_end_idx=interval["left"][1],
                    right_start_idx=interval["right"][0],
                    right_end_idx=interval["right"][1],
                )
                self._animation_manager.sort_two_groups_animation(
                    sorting_object=self._sorting_object,
                    source_indices=list(range(interval["left"][0], interval["right"][1]+1)),
                    target_indices=target_indices,
                )
                self._animation_manager.deselect_interval_animation(
                    sorting_object=self._sorting_object,
                    idx_left=interval["left"][0],
                    idx_right=interval["right"][1],
                )
                self._sorting_object[interval["left"][0]:interval["right"][1]+1] = [self._sorting_object.get_bar(idx=idx) for idx in target_indices]

    @staticmethod
    def split(d: dict, left_idx: int, right_idx: int, level: int):

        if (right_idx - left_idx) <= 0:
            return

        left_idx_end = left_idx + (right_idx - left_idx) // 2
        right_idx_start = left_idx_end + 1

        if level not in d:
            d[level] = []
        d[level].append({"left": (left_idx, left_idx_end), "right": (right_idx_start, right_idx)})

        MergeSort.split(d=d, left_idx=left_idx, right_idx=left_idx_end, level=level + 1)
        MergeSort.split(d=d, left_idx=right_idx_start, right_idx=right_idx, level=level + 1)


    @staticmethod
    def merge(arr, left_start_idx, left_end_idx, right_start_idx, right_end_idx):

        left_idx = left_start_idx
        right_idx = right_end_idx
        temp_arr = [0] * (right_idx - left_idx)
        arr_indices = []
        idx = 0
        while True:

            if arr[left_start_idx] <= arr[right_start_idx]:
                temp_arr[idx] = arr[left_start_idx]
                arr_indices.append(left_start_idx)
                left_start_idx += 1
                idx += 1
            else:
                temp_arr[idx] = arr[right_start_idx]
                arr_indices.append(right_start_idx)
                right_start_idx += 1
                idx += 1

            if left_start_idx > left_end_idx:
                temp_arr[idx:] = arr[right_start_idx:right_end_idx+1]
                arr_indices.extend(list(range(right_start_idx, right_end_idx+1)))
                break
            if right_start_idx > right_end_idx:
                temp_arr[idx:] = arr[left_start_idx:left_end_idx+1]
                arr_indices.extend(list(range(left_start_idx, left_end_idx+1)))
                break

        arr[left_idx:right_idx+1] = temp_arr
        return arr_indices





