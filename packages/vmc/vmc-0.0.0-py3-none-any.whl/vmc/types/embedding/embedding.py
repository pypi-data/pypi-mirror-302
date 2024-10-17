from typing import List, Dict

from .._base import BaseOutput


class EmbeddingOutput(BaseOutput):
    embeddings: List[List[float]] | None = None
    weights: List[Dict[int, float]] | None = None
