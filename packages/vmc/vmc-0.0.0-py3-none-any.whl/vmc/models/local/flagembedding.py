from vmc.models._base import BaseEmbeddingModel
from vmc.types.embedding import EmbeddingOutput
from typing import Optional, Dict, List, Any
from FlagEmbedding import BGEM3FlagModel
from pydantic import BaseModel


class BGEM3ModelInput(BaseModel):
    sentences: List[str] | str
    batch_size: int = 12
    max_length: int = 8192
    return_dense: bool = True
    return_sparse: bool = False
    return_colbert_vecs: bool = False


class BGEM3Model(BaseEmbeddingModel):
    model: Optional[Any] = None
    batch_size: int = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model: BGEM3FlagModel = BGEM3FlagModel(self.model_id)

    def _prepare_model_inputs(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ):
        return BGEM3ModelInput(
            sentences=prompt, batch_size=self.batch_size, **parameters
        ).model_dump()

    def _get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        output = self.model.encode(**self._prepare_model_inputs(prompt, parameters))
        dense = output["dense_vecs"]
        if dense is not None:
            dense = [dense] if isinstance(prompt, str) else dense
        weights = output["lexical_weights"]
        if weights is not None:
            weights = [weights] if isinstance(prompt, str) else weights
        return EmbeddingOutput(embeddings=dense, weights=weights)
