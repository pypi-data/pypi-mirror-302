import os
import random
from typing import Any, AsyncGenerator, Dict, List, Union

import google.generativeai as genai

from vmc.types.chat import (
    BaseMessage,
    TextGenerationDetails,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
)
from vmc.types.embedding import EmbeddingOutput
from vmc.utils.proxy import use_proxy
from .._base import BaseChatModel, BaseEmbeddingModel


def convert_dicts_to_glm(d: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    role_map = {"user": "user", "bot": "bot", "system": "model", "assistant": "model"}
    return [
        {"role": role_map.get(m["role"], "model"), "parts": [m["content"]]} for m in d
    ]


class GeminiModel(BaseChatModel, BaseEmbeddingModel):
    model: str = "gemini-pro"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure_model(self):
        genai.configure(api_key=random.choice(self.credentials)["api_key"])
        return genai.GenerativeModel(self.model)

    def _prepare_chat_args(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        if isinstance(prompt, str):
            messages = convert_dicts_to_glm(parameters.pop("history", [])) + [
                {"role": "user", "parts": [prompt]}
            ]
        else:
            messages = [
                m.model_dump() if isinstance(m, BaseMessage) else m for m in prompt
            ]
            parameters.pop("history", [])
        if "max_tokens" in parameters:
            parameters["max_output_tokens"] = parameters.pop("max_tokens")
        parameters.pop("frequency_penalty", None)
        parameters.pop("presence_penalty", None)
        return {
            "contents": messages,
            "generation_config": parameters,
        }

    async def _achat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> TextGenerationOutput:
        model = self.configure_model()
        with use_proxy():
            response = await model.generate_content_async(
                **self._prepare_chat_args(prompt, parameters)
            )
        return TextGenerationOutput(
            generated_text=response.text,
            details=TextGenerationDetails(model=self.model),
        )

    async def _astream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        model = self.configure_model()
        os.environ["http_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        os.environ["https_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        response = await model.generate_content_async(
            **self._prepare_chat_args(prompt, parameters), stream=True
        )

        async for chunk in response:
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(text=chunk.text),
                details=TextGenerationDetails(model=self.model),
            )
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")

    async def _a_n_toknens(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> int:
        model = self.configure_model()
        os.environ["http_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        os.environ["https_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        res = await model.count_tokens_async(
            **self._prepare_chat_args(prompt, parameters)
        )
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")
        return res.total_tokens

    def _get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        task_type = parameters.pop("task_type", "retrieval_document")
        title = parameters.pop("title", None)
        if task_type == "retrieval_document" and title is None:
            raise ValueError(
                "The `title` parameter must be specified when `task_type` is `retrieval_document`"
            )
        os.environ["http_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        os.environ["https_proxy"] = os.getenv("OPENAI_HTTP_PROXY")
        result = genai.embed_content(
            model="models/embedding-001",
            title=title,
            content=prompt,
            task_type=task_type,
        )
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")
        if isinstance(prompt, str):
            return EmbeddingOutput(embeddings=[result["embedding"]])
        return EmbeddingOutput(embeddings=result["embedding"])
