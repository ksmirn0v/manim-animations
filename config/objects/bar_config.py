from pydantic import BaseModel, Field, ConfigDict


class BarConfig(BaseModel):

    fill_color: str = Field(default='#bbbbbb')
    fill_opacity: float = Field(default=1.0)
    stroke_color: str = Field(default='#ffffff')
    stroke_opacity: float = Field(default=1.0)
    stroke_width_px: int = Field(default=4)
    corner_radius_local: float
    width_local: float
    height_local: float
    number_scale_local: float
    gap_between_rect_and_number_local: float

    model_config = ConfigDict(
        alias_generator=lambda x: x.upper(),
        populate_by_name=True,
    )
