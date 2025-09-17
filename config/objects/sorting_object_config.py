from pydantic import BaseModel, ConfigDict


class SortingObjectConfig(BaseModel):

    gap_between_bars_local: float
    distance_to_edge_local: float

    model_config = ConfigDict(
        alias_generator=lambda x: x.upper(),
        populate_by_name=True,
    )
