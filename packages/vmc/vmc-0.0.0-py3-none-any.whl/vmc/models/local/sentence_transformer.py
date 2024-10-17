from vmc.types.embedding import EmbeddingOutput
from vmc.types.rerank import CrossEncoderOutput
from vmc.types.errors import errors as err
from vmc.models._base import BaseCrossEncoderModel, BaseEmbeddingModel
from typing import Optional, Dict, List, Any
from vmc.utils.utils import torch_gc
from sentence_transformers import SentenceTransformer, CrossEncoder
from vmc.types.rerank import RerankModelParams
from tqdm import tqdm


class CrossEncoderModel(BaseCrossEncoderModel):
    model: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = CrossEncoder(self.model_id, device="cuda")

    def _predict(
        self, sentences: List[List[str]], parameters: RerankModelParams = {}
    ) -> CrossEncoderOutput:
        try:
            scores = (
                self.model.predict(sentences, **parameters).tolist()
                if sentences
                else []
            )
            return CrossEncoderOutput(scores=scores)
        except Exception as e:
            raise err.InternalServerError(msg=str(e)) from None


class SentenceTransformerModel(BaseEmbeddingModel):
    normalize_embeddings: bool = False
    max_tokens: int = -1
    prefix: str = ""
    model: Optional[Any] = None
    batch_size: int = 64

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = SentenceTransformer(
            self.model_id, device="cuda", trust_remote_code=True
        )
        self.model.eval()

    def _get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        prompt = [prompt] if isinstance(prompt, str) else prompt
        parameters = {"normalize_embeddings": self.normalize_embeddings, **parameters}
        prefix = parameters.pop("prefix", self.prefix)
        prompt = [prefix + p for p in prompt]
        embeddings = []
        for i in tqdm(range(0, len(prompt), self.batch_size), desc="Batch Embedding"):
            embeddings.extend(
                self.model.encode(
                    prompt[i : i + self.batch_size], **parameters
                ).tolist()
            )
            torch_gc()

        return EmbeddingOutput(embeddings=embeddings)
