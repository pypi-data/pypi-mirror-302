import os
import random
from typing import Any, Dict, List, Union

import httpx
import tiktoken
from openai import AsyncOpenAI
from openai.types.chat import CompletionCreateParams

from vmc.utils.utils import o2g, o2s
from vmc.models._base import BaseChatModel, BaseEmbeddingModel
from vmc.types.chat import BaseMessage, TextGenerationOutput
from vmc.types.embedding import EmbeddingOutput


class ChatOpenAI(BaseChatModel, BaseEmbeddingModel):
    model: str = "gpt-3.5-turbo"
    proxies: dict[str, str] = {}
    transform_first_message: bool = False

    def _setup_client(self):
        credential = random.choice(self.credentials)
        if not self.proxies:
            self.proxies = {
                "http_proxy://": os.getenv("OPENAI_HTTP_PROXY", None),
                "https_proxy://": os.getenv("OPENAI_HTTPS_PROXY", None),
                "all://": os.getenv("OPENAI_ALL_PROXY", None),
            }
        params = {
            "api_key": credential["api_key"],
            "max_retries": 5,
            "timeout": httpx.Timeout(timeout=600.0, connect=30.0),
            "base_url": credential.get("base_url", None),
            "http_client": httpx.AsyncClient(proxies=self.proxies),
        }
        return AsyncOpenAI(**params)

    def n_tokens(self, prompt: str, parameters: Dict[str, Any]) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(prompt, **parameters))

    async def _aopenai_chat(self, req: CompletionCreateParams):
        client = self._setup_client()
        req["model"] = self.model
        return await client.chat.completions.create(**req)

    def _prepare_chat_args(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: dict,
        stream: bool = False,
    ):
        if isinstance(prompt, str):
            messages = parameters.pop("history", []) + [
                {"role": "user", "content": prompt}
            ]
        else:
            messages = [
                m.model_dump() if isinstance(m, BaseMessage) else m for m in prompt
            ]
            parameters.pop("history", [])
        if self.transform_first_message:
            if len(messages) == 1 and messages[0]["role"] == "system":
                messages[0]["role"] = "user"
        parameters = {**self.config.default_params, **parameters}
        parameters["messages"] = messages
        parameters["model"] = self.model
        parameters["stream"] = stream
        if "frequency_penalty" in parameters and "baichuan" in self.model.lower():
            """baichuan model has a different frequency penalty(1-2)"""
            parameters["frequency_penalty"] = parameters["frequency_penalty"] + 1
        return parameters

    async def _achat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> TextGenerationOutput:
        client = self._setup_client()
        completion = await client.chat.completions.create(
            **self._prepare_chat_args(prompt, parameters)
        )

        return o2g(completion)

    async def _astream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ):
        client = self._setup_client()
        async for delta in await client.chat.completions.create(
            **self._prepare_chat_args(prompt, parameters=parameters, stream=True)
        ):
            if len(delta.choices) == 0 or delta.choices[0].delta.content is None:
                continue
            yield o2s(delta)

    async def _aget_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        client = self._setup_client()
        embed_out = await client.embeddings.create(
            input=prompt, model=self.model, **parameters
        )
        return EmbeddingOutput(embeddings=[x.embedding for x in embed_out.data])
