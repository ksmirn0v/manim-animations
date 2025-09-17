from typing import Dict, Any

from pydantic import BaseModel


class AlgorithmConfig(BaseModel):

    parameters: Dict[str, Any]
