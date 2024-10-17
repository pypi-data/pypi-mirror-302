from typing import Any, AsyncGenerator, Dict, List, Union

from openai.types.audio.transcription_create_params import TranscriptionCreateParams

from vmc.types.chat import (
    LMParameters,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    BaseMessage,
)
from vmc.types.embedding import EmbeddingOutput
from vmc.types.audio import Transcription
from vmc.types.rerank import CrossEncoderOutput, RerankModelParams

from modelhub import ModelhubClient
from .._base import BaseChatModel, BaseCrossEncoderModel, BaseEmbeddingModel
from ..local.whisper import BaseAudioModel
import requests


class ModelhubModel(
    BaseChatModel, BaseAudioModel, BaseCrossEncoderModel, BaseEmbeddingModel
):
    host: str = "http://127.0.0.1"
    model_id: str

    client: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = ModelhubClient(host=self.host, user_name="", user_password="")

    def alive(self) -> bool:
        try:
            res = requests.get(f"{self.host}/ping")
        except Exception:
            return False
        return res.status_code == 200

    async def _achat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = [],
    ) -> TextGenerationOutput:
        return await self.client.achat(
            prompt,
            self.model_id,
            parameters.pop("history", []),
            parameters.pop("return_type", "text"),
            parameters.pop("schema", None),
            parameters,
        )

    async def _astream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = [],
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        self._pop_custom_parameters(parameters)
        async for chunk in self.client.astream_chat(
            prompt,
            self.model_id,
            parameters.pop("history", []),
            parameters,
        ):
            yield chunk

    async def _aget_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        return await self.client.aget_embeddings(prompt, self.model_id, parameters)

    async def _atranscribe(self, req: TranscriptionCreateParams) -> Transcription:
        return await self.client.atranscribe(
            req["file"], req["model"], req["language"], req["temperature"]
        )

    async def _apredict(
        self, sentences: List[List[str]], parameters: RerankModelParams
    ) -> CrossEncoderOutput:
        return await self.client.across_embedding(sentences, self.model_id, parameters)
