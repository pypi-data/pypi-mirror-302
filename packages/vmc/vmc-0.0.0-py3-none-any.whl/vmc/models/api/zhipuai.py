from typing import Any, Dict, Generator, List, Union

from zhipuai import ZhipuAI
from zhipuai.types.chat.chat_completion import Completion
from zhipuai.types.chat.chat_completion_chunk import ChatCompletionChunk
from pydantic.v1 import BaseModel, Field

from vmc.types.chat import (
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationDetails,
    TextGenerationStreamToken,
    BaseMessage,
    ToolCallOutput,
)
from vmc.types.embedding import EmbeddingOutput
from vmc.models._base import BaseChatModel, BaseEmbeddingModel
import random


class ZhipuChatParams(BaseModel):
    model: str
    request_id: str | None = None
    do_sample: bool | None = None
    stream: bool | None = None
    temperature: float = Field(gt=0, le=1, default=0.95)
    top_p: float = Field(gt=0, lt=1, default=0.7)
    max_tokens: int | None = None
    seed: int | None = None
    messages: str | list[str] | list[int] | object | None
    stop: str | list[str] | None = None
    sensitive_word_check: object | None = None
    tools: object | None = None
    tool_choice: str | None = None


def z2g(c: Completion) -> TextGenerationOutput:
    """Transform OpenAI Completion to TextGeneration"""
    tool_calls = c.choices[0].message.tool_calls
    print(tool_calls)
    return TextGenerationOutput(
        generated_text=c.choices[0].message.content,
        tool_calls=[ToolCallOutput.model_validate(tc.model_dump()) for tc in tool_calls]
        if tool_calls
        else None,
        details=TextGenerationDetails(
            finish_reason=c.choices[0].finish_reason or "stop",
            created=c.created,
            model=c.model,
            prompt_tokens=c.usage.prompt_tokens,
            generated_tokens=c.usage.completion_tokens,
        ),
    )


def z2s(c: ChatCompletionChunk) -> TextGenerationStreamOutput:
    """Transform OpenAI CompletionChunk to TextGeneration"""
    tool_calls = c.choices[0].delta.tool_calls
    return TextGenerationStreamOutput(
        token=TextGenerationStreamToken(text=c.choices[0].delta.content),
        tool_calls=[ToolCallOutput.model_validate(tc.model_dump()) for tc in tool_calls]
        if tool_calls
        else None,
        details=TextGenerationDetails(
            finish_reason=c.choices[0].finish_reason or "stop",
            created=c.created,
            model=c.model,
        ),
    )


class ZhipuAIModel(BaseChatModel, BaseEmbeddingModel):
    model: str = "glm-4"

    def _setup_client(self):
        api_key = random.choice(self.credentials)["api_key"]
        return ZhipuAI(api_key=api_key)

    def _prepare_chat_args(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        parameters.pop("top_k", None)
        parameters.pop("frequency_penalty", None)
        parameters.pop("presence_penalty", None)
        if isinstance(prompt, str):
            messages = parameters.pop("history", []) + [
                {"role": "user", "content": prompt}
            ]
        else:
            messages = [
                m.model_dump() if isinstance(m, BaseMessage) else m for m in prompt
            ]
            parameters.pop("history", [])
        if len(messages) == 1 and messages[0]["role"] == "system":
            messages[0]["role"] = "user"
        return {
            "model": self.model,
            "messages": messages,
            **parameters,
        }

    def _chat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> TextGenerationOutput:
        client = self._setup_client()
        return z2g(
            client.chat.completions.create(
                **self._prepare_chat_args(prompt, parameters)
            )
        )

    def _stream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        client = self._setup_client()
        response = client.chat.completions.create(
            **self._prepare_chat_args(prompt, parameters),
            stream=True,
        )

        for delta in response:
            if len(delta.choices) == 0 or delta.choices[0].delta.content is None:
                continue
            yield z2s(delta)

    def _prepare_embedding_args(self, parameters: dict):
        """encoding_format: str | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        request_id: str | NotGiven | None = NOT_GIVEN,
        sensitive_word_check: object | NotGiven | None = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_body: Any | None = None,
        disable_strict_validation: bool | None = None"""
        ret = {}
        potential_args = [
            "encoding_format",
            "user",
            "request_id",
            "sensitive_word_check",
            "extra_headers",
            "extra_body",
            "disable_strict_validation",
        ]
        for key in potential_args:
            if key in parameters:
                ret[key] = parameters[key]
        return ret

    def _get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        client = self._setup_client()
        embed_out = client.embeddings.create(
            input=prompt, model=self.model, **self._prepare_embedding_args(parameters)
        )
        return EmbeddingOutput(embeddings=[x.embedding for x in embed_out.data])
