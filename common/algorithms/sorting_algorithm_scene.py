import constants
from common.algorithms import AlgorithmScene
from common.animations.animation_manager_factory import AnimationManagerFactory
from constants import names
from objects.bar import Bar
from objects.sorting_object import SortingObject


class SortingAlgorithmScene(AlgorithmScene):

    def set_initial_variables(self):

        self._values = constants.CONFIG.get_parameters(name=names.VALUES)
        self._animation_manager = AnimationManagerFactory.create(
            scene=self,
            config=constants.CONFIG.get_parameters(name=names.ANIMATIONS),
        )

    def run_initial_animation(self):

        self._bars = [Bar(value=value, config=constants.CONFIG.get_parameters(name=names.BAR)) for value in self._values]
        self._sorting_object = SortingObject(bars=self._bars, config=constants.CONFIG.get_parameters(name=names.SORTING_OBJECT))
        self._sorting_object.set_y(0.0)

        self._animation_manager.fade_in_animation(sorting_object=self._sorting_object)
        self.wait(0.5)

    def run_end_animation(self):

        self._animation_manager.fade_out_animation(sorting_object=self._sorting_object)
