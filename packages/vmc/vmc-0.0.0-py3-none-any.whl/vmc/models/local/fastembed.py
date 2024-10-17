from typing import Any, Dict, List, Optional

from fastembed import SparseTextEmbedding

from vmc.utils import proxy
from vmc.models._base import BaseEmbeddingModel
from vmc.types.embedding import EmbeddingOutput


class FastEmbedSparseTextEmbedding(BaseEmbeddingModel):
    model: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        paths = self.model_id.split("/")
        model_id = "/".join(paths[-2:])
        cache_dir = self.model_id[: -len(model_id)]
        with proxy.use_proxy():
            self.model = SparseTextEmbedding(model_name=model_id, cache_dir=cache_dir)

    def _prepare_model_inputs(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ):
        return {"documents": prompt}

    def _get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        output = list(
            self.model.embed(**self._prepare_model_inputs(prompt, parameters))
        )
        return EmbeddingOutput(
            weights=[{i: v for i, v in zip(e.indices, e.values)} for e in output]
        )
