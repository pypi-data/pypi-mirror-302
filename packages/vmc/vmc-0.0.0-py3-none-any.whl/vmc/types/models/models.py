from typing import Dict, List, Literal

from .._base import BaseModel, BaseOutput


class ModelInfo(BaseModel):
    types: List[Literal["chat", "embedding", "audio", "reranker"]]

    class Config:
        extra = "allow"


class ModelInfoOutput(BaseOutput):
    models: Dict[str, ModelInfo]
