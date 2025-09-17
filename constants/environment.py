import os
from models import AlgorithmName, VideoType


ALGORITHM_NAME = AlgorithmName[os.environ.get("ALGORITHM_NAME").upper()]
VIDEO_TYPE = VideoType[os.environ.get("VIDEO_TYPE").upper()]