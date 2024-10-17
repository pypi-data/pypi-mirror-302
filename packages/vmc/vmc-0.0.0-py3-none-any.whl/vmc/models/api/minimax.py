import json
from typing import Any, AsyncGenerator, Dict, List, Union

import httpx
import retrying
from pydantic.v1 import BaseModel
from loguru import logger

from vmc.types.chat import (
    TextGenerationDetails,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    BaseMessage,
)
from vmc.types.embedding import EmbeddingOutput
from .._base import BaseChatModel, BaseEmbeddingModel
import random


class _MinimaxEndpointClient(BaseModel):
    group_id: str
    api_key: str
    api_url: str = ""
    host: str
    timeout: float = 600.0
    max_attempts: int = 5
    retry_delay: int = 2000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = f"{self.host}/v1/text/chatcompletion_pro?GroupId={self.group_id}"

    @retrying.retry(stop_max_attempt_number=max_attempts, wait_fixed=retry_delay)
    async def astream(self, request: Any) -> Any:
        logger.debug(f"Request: {request}")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        request["use_standard_sse"] = True
        request["stream"] = True
        async with httpx.AsyncClient() as client:
            async with client.stream(
                method="post",
                url=self.api_url,
                headers=headers,
                timeout=self.timeout,
                json=request,
            ) as response:
                async for chunk in response.aiter_lines():
                    try:
                        chunk = json.loads(chunk[5:])
                        yield chunk
                    except Exception:
                        pass

    @retrying.retry(stop_max_attempt_number=max_attempts, wait_fixed=retry_delay)
    async def apost(self, request: Any) -> Any:
        logger.debug(f"Request: {request}")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url, headers=headers, json=request, timeout=self.timeout
            )
            response.raise_for_status()
            if response.json()["base_resp"]["status_code"] > 0:
                raise ValueError(
                    f"API {response.json()['base_resp']['status_code']}"
                    f" error: {response.json()['base_resp']['status_msg']}"
                )
            return response.json()["reply"]

    @retrying.retry(stop_max_attempt_number=max_attempts, wait_fixed=retry_delay)
    async def aget_embeddings(self, request: Any) -> Any:
        embedding_api_url = (
            f"https://api.minimax.chat/v1/embeddings?GroupId={self.group_id}"
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        request["model"] = "embo-01"  # max tokens is 4096
        request["type"] = request.get("type", "query")
        assert request["type"] in ["db", "query"]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                embedding_api_url, headers=headers, json=request, timeout=self.timeout
            )
            if not response.ok:
                raise ValueError(f"HTTP {response.status_code} error: {response.text}")
            if response.json()["base_resp"]["status_code"] > 0:
                raise ValueError(
                    f"API {response.json()['base_resp']['status_code']}"
                    f" error: {response.json()['base_resp']['status_msg']}"
                )
            return response.json()["vectors"]


class Minimax(BaseChatModel, BaseEmbeddingModel):
    """
    Minimax chat model
    documentation: https://api.minimax.chat/document
    """

    client: Any = None
    model: str = "abab5.5-chat"

    def setup_client(self):
        credential = random.choice(self.credentials)
        api_key = credential["api_key"]
        group_id = credential["group_id"]
        self.client = _MinimaxEndpointClient(
            host="https://api.minimax.chat", api_key=api_key, group_id=group_id
        )

    def _prepare_chat_args(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        if isinstance(prompt, str):
            prompt = [{"sender_type": "USER", "sender_name": "user", "text": prompt}]
        else:
            minimax_messages = []
            for m in prompt:
                if isinstance(m, dict):
                    m = BaseMessage(**m)
                if m.role == "user":
                    minimax_messages.append(
                        {
                            "sender_type": "USER",
                            "sender_name": "user",
                            "text": m.content,
                        }
                    )
                elif m.role == "assistant":
                    minimax_messages.append(
                        {
                            "sender_type": "BOT",
                            "user_name": "MM智能助理",
                            "text": m.content,
                        }
                    )
            prompt = minimax_messages
        parameters.pop("history", [])
        parameters.pop("frequency_penalty", None)
        parameters.pop("presence_penalty", None)
        parameters["model"] = self.model
        if "max_tokens" in parameters:
            parameters["tokens_to_generate"] = parameters.pop("max_tokens")
        return {
            "request": {
                "messages": prompt,
                "bot_setting": [
                    {
                        "bot_name": "MM智能助理",
                        "content": "MM智能助理是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。",
                    }
                ],
                "reply_constraints": {
                    "sender_type": "BOT",
                    "sender_name": "MM智能助理",
                },
                **parameters,
            }
        }

    async def _achat(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationOutput:
        self.setup_client()
        return TextGenerationOutput(
            generated_text=await self.client.apost(
                **self._prepare_chat_args(prompt, parameters)
            ),
            details=TextGenerationDetails(model=self.model),
        )

    async def _astream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        self.setup_client()
        async for chunk in self.client.astream(
            **self._prepare_chat_args(prompt, parameters)
        ):
            if len(chunk["choices"]) == 0:
                continue
            delta = chunk["choices"][0]["delta"]
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(text=delta),
                details=TextGenerationDetails(model=self.model),
            )

    async def _aget_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        self.setup_client()
        prompt = [prompt] if isinstance(prompt, str) else prompt
        requests = {
            "texts": prompt,
            **parameters,
        }
        return EmbeddingOutput(embeddings=await self.client.aget_embeddings(requests))
