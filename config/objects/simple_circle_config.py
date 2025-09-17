from pydantic import BaseModel, ConfigDict, Field


class SimpleCircleConfig(BaseModel):

    radius_local: float
    stroke_width_px: int = Field(default=4)

    model_config = ConfigDict(
        alias_generator=lambda x: x.upper(),
        populate_by_name=True,
    )
