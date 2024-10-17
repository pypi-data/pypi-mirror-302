from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from vmc.utils.utils import torch_gc
from vmc.models._base import BaseEmbeddingModel
from vmc.types.embedding import EmbeddingOutput
from vmc.utils.proxy import use_proxy


class JinaParams(BaseModel):
    task_type: str


class JinaEmbedding(BaseEmbeddingModel):
    """Extended Sequence Length: Supports up to 8192 tokens with RoPE.
    Task-Specific Embedding: Customize embeddings through the task argument with the following options:
        retrieval.query: Used for query embeddings in asymmetric retrieval tasks
        retrieval.passage: Used for passage embeddings in asymmetric retrieval tasks
        separation: Used for embeddings in clustering and re-ranking applications
        classification: Used for embeddings in classification tasks
        text-matching: Used for embeddings in tasks that quantify similarity between two texts, such as STS or symmetric retrieval tasks

    Matryoshka Embeddings: Supports flexible embedding sizes (32, 64, 128, 256, 512, 768, 1024), allowing for truncating embeddings to fit your application."""

    max_tokens: int = 8192
    prefix: str = ""
    model: Optional[Any] = None
    batch_size: int = 64

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with use_proxy():
            self.model = SentenceTransformer(
                self.model_id, trust_remote_code=True, device="cuda"
            ).eval()

    def _get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        prompt = [prompt] if isinstance(prompt, str) else prompt
        prefix = parameters.pop("prefix", self.prefix)
        prompt = [prefix + p for p in prompt]
        task_type = parameters.pop("task_type", "retrieval.query")

        embeddings = []
        for i in tqdm(range(0, len(prompt), self.batch_size), desc="Batch Embedding"):
            embeddings.extend(
                self.model.encode(
                    sentences=prompt[i : i + self.batch_size],
                    task=task_type,
                    prompt_name=task_type,
                ).tolist()
            )
            torch_gc()

        return EmbeddingOutput(embeddings=embeddings)
