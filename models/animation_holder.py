from dataclasses import dataclass

from manim import Animation

from models.animation_id import AnimationId


@dataclass
class AnimationHolder:

    id: AnimationId
    animation: Animation
