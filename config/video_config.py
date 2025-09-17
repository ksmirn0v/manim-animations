from pydantic import BaseModel, field_validator


class VideoConfig(BaseModel):

    pixel_width: int
    pixel_height: int
    frame_height: float
    frame_width: float
    frame_rate: float
    output_file: str

    @field_validator('frame_height', 'frame_width', mode='before')
    @classmethod
    def parse_frame_height(cls, frame_parameter: str | float):
        if isinstance(frame_parameter, str):
            return float(eval(frame_parameter))
        return frame_parameter
