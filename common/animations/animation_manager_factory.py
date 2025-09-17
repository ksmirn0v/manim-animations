from manim import Scene

import constants
from algorithms.selection_sort.animations import AnimationManager as AnimationManagerSelectioSort
from algorithms.bubble_sort.animations import AnimationManager as AnimationManagerBubbleSort
from algorithms.merge_sort.animations import AnimationManager as AnimationManagerMergeSort
from algorithms.quick_sort.animations import AnimationManager as AnimationManagerQuickSort
from models import AlgorithmName


class AnimationManagerFactory:

    @staticmethod
    def create(scene: Scene, config: dict):

        algorithm_name = constants.ALGORITHM_NAME
        if algorithm_name == AlgorithmName.SELECTION_SORT:
            return AnimationManagerSelectioSort(scene=scene, config=config)
        if algorithm_name == AlgorithmName.BUBBLE_SORT:
            return AnimationManagerBubbleSort(scene=scene, config=config)
        if algorithm_name == AlgorithmName.MERGE_SORT:
            return AnimationManagerMergeSort(scene=scene, config=config)
        if algorithm_name == AlgorithmName.QUICK_SORT:
            return AnimationManagerQuickSort(scene=scene, config=config)
        return None
