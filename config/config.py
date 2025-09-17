import os
import yaml

from manim import config as manim_config

import constants
from config import VideoConfig, AlgorithmConfig
from constants import names


class Config:

    def __init__(self):

        with open(os.path.join("config", "config.yaml"), "r") as file:
            video_config: dict = yaml.safe_load(file)

        algorithm_config_name = constants.ALGORITHM_NAME
        algorithm_config_file_path = os.path.join('algorithms', algorithm_config_name.value, 'config.yaml')
        with open(algorithm_config_file_path, 'r') as file:
            algorithm_config: dict = yaml.safe_load(file)

        config = self._compile_config(video_config=video_config, algorithm_config=algorithm_config)
        self._video = VideoConfig(**config[names.VIDEO][names.PARAMETERS], output_file=algorithm_config_name.value)
        self._algorithm = AlgorithmConfig(parameters=config[names.ALGORITHM][names.PARAMETERS])
        self._apply_video_config()

    def get_parameters(self, name: str):

        return self._algorithm.parameters[name]

    def _apply_video_config(self):

        manim_config.pixel_width = self._video.pixel_width
        manim_config.pixel_height = self._video.pixel_height
        manim_config.frame_height = self._video.frame_height
        manim_config.frame_width = self._video.frame_width
        manim_config.frame_rate = self._video.frame_rate
        manim_config.output_file = self._video.output_file

    @staticmethod
    def _compile_config(video_config: dict, algorithm_config: dict) -> dict:

        final_config = {names.VIDEO: {}, names.ALGORITHM: {}}

        video_type = constants.VIDEO_TYPE.value

        if video_config[names.TARGETS][video_type] is not None:
            for key in video_config[names.TARGETS][video_type]:
                if key in video_config[names.PARAMETERS]:
                    video_config[names.PARAMETERS][key] = video_config[names.TARGETS][video_type][key]

        final_config[names.VIDEO][names.PARAMETERS] = video_config[names.PARAMETERS]

        if algorithm_config[names.TARGETS][video_type] is not None:
            for key in algorithm_config[names.TARGETS][video_type]:
                if isinstance(algorithm_config[names.PARAMETERS][key], dict):
                    for internal_key in algorithm_config[names.TARGETS][video_type][key]:
                        algorithm_config[names.PARAMETERS][key][internal_key] = algorithm_config[names.TARGETS][video_type][key][internal_key]
                else:
                    algorithm_config[names.PARAMETERS][key] = algorithm_config[names.TARGETS][video_type][key]

        final_config[names.ALGORITHM][names.PARAMETERS] = algorithm_config[names.PARAMETERS]

        return final_config

    @staticmethod
    def _parse_value_from_formula(value: str | float) -> float:

        return eval(value) if isinstance(value, str) else value
