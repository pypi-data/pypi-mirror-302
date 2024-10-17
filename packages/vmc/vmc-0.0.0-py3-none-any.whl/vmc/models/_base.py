import inspect
from abc import ABC
from typing import Any, AsyncGenerator, Coroutine, Dict, Generator, List, Union

import anyio
from loguru import logger
from openai.types.audio.transcription_create_params import TranscriptionCreateParams
from openai.types.chat import CompletionCreateParams
from openai.types.create_embedding_response import CreateEmbeddingResponse, Usage
from openai.types.embedding import Embedding
from openai.types.embedding_create_params import EmbeddingCreateParams
from pydantic.v1 import BaseModel

from vmc.config import ModelConfig
from vmc.exception import exception_handler
from vmc.utils.utils import (
    g2o,
    prepare_modelhub_args,
    s2o,
    torch_gc,
)
from vmc.types.audio import Transcription
from vmc.types.chat import (
    BaseMessage,
    LMParameters,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
)
from vmc.types.embedding import EmbeddingOutput
from vmc.types.rerank import CrossEncoderOutput, RerankModelParams


class BaseModelhubModel(BaseModel, ABC):
    model_id: str = ""
    """
    local model path, remote model id
    """
    config: ModelConfig
    credentials: list[dict] | None = None


def local_model_support(func):
    def generator_wrapper(self, *args, **kwargs):
        try:
            if self.config.is_local:
                torch_gc()
            for res in func(self, *args, **kwargs):
                yield res
        except Exception as e:
            msg = anyio.run(
                exception_handler,
                e,
                {
                    "model": self.config.name,
                    **kwargs,
                    "args": args,
                },
            )
            yield msg.e()
            return
        finally:
            if self.config.is_local:
                torch_gc()

    def wrapper(self, *args, **kwargs):
        try:
            if self.config.is_local:
                torch_gc()
            return func(self, *args, **kwargs)
        except Exception as e:
            if hasattr(e, "context"):
                e.context.update(
                    {
                        "model": self.config.name,
                        **kwargs,
                        "args": args,
                    }
                )
            else:
                e.__setattr__(
                    "context",
                    {
                        "model": self.config.name,
                        **kwargs,
                        "args": args,
                    },
                )
            raise e from None
        finally:
            if self.config.is_local:
                torch_gc()

    async def coroutine_wrapper(self, *args, **kwargs):
        try:
            if self.config.is_local:
                torch_gc()
            return await func(self, *args, **kwargs)
        except Exception as e:
            if hasattr(e, "context"):
                e.context.update(
                    {
                        "model": self.config.name,
                        **kwargs,
                        "args": args,
                    }
                )
            else:
                e.__setattr__(
                    "context",
                    {
                        "model": self.config.name,
                        **kwargs,
                        "args": args,
                    },
                )
            raise e from None
        finally:
            if self.config.is_local:
                torch_gc()

    async def async_gen_wrapper(self, *args, **kwargs):
        try:
            if self.config.is_local:
                torch_gc()
            async for res in func(self, *args, **kwargs):
                yield res
        except Exception as e:
            msg = await exception_handler(
                e,
                {
                    "model": self.config.name,
                    **kwargs,
                    "args": args,
                },
            )
            yield msg.e()
            return
        finally:
            if self.config.is_local:
                torch_gc()

    if inspect.isasyncgenfunction(func):
        return async_gen_wrapper
    elif inspect.iscoroutinefunction(func):
        return coroutine_wrapper
    elif inspect.isgeneratorfunction(func):
        return generator_wrapper
    else:
        return wrapper


class BaseCrossEncoderModel(BaseModelhubModel, ABC):
    def _predict(self, sentences: List[List[str]], parameters: RerankModelParams):
        raise NotImplementedError("predict is not supported for this model")

    async def _apredict(
        self, sentences: List[List[str]], parameters: RerankModelParams
    ):
        return await anyio.to_thread.run_sync(self._predict, sentences, parameters)

    @local_model_support
    async def apredict(
        self, sentences: List[List[str]], parameters: RerankModelParams
    ) -> CrossEncoderOutput:
        return await self._apredict(sentences, parameters)


class BaseAudioModel(BaseModelhubModel):
    def _transcribe(self, req: TranscriptionCreateParams) -> Transcription:
        raise NotImplementedError("transcribe is not supported for this model")

    async def _atranscribe(self, req: TranscriptionCreateParams) -> Transcription:
        return await anyio.to_thread.run_sync(self._transcribe, req)

    @local_model_support
    async def atranscribe(self, req: TranscriptionCreateParams) -> Transcription:
        return await self._atranscribe(req)


class BaseEmbeddingModel(BaseModelhubModel, ABC):
    def _get_embeddings(
        self,
        prompt: Union[str, List[BaseMessage]] | List[str],
        parameters: Dict[str, Any] = {},
    ) -> EmbeddingOutput:
        """Get embeddings from a model"""
        raise NotImplementedError("Embeddings are not supported for this model")

    async def _aget_embeddings(
        self,
        prompt: str | List[str],
        parameters: Dict[str, Any] = {},
    ) -> EmbeddingOutput:
        """Get embeddings from a model"""
        return await anyio.to_thread.run_sync(self._get_embeddings, prompt, parameters)

    @local_model_support
    async def aget_embeddings(
        self,
        prompt: str | List[str],
        parameters: Dict[str, Any] = {},
    ) -> EmbeddingOutput:
        """Get embeddings from a model"""
        return await self._aget_embeddings(prompt=prompt, parameters=parameters)

    async def _aget_embeddings_openai(
        self, params: EmbeddingCreateParams
    ) -> CreateEmbeddingResponse:
        """Get embeddings from a model"""
        _params = params.copy()
        _params.pop("model", None)
        _input = _params.pop("input", None)
        embeddings = (await self.aget_embeddings(_input, _params)).embeddings
        embeddings = [
            Embedding(embedding=embedding, index=i, object="embedding")
            for i, embedding in enumerate(embeddings)
        ]
        return CreateEmbeddingResponse(
            data=embeddings,
            model=params["model"],
            object="list",
            usage=Usage(prompt_tokens=0, total_tokens=0),
        )

    @local_model_support
    async def aget_embeddings_openai(
        self, params: EmbeddingCreateParams
    ) -> CreateEmbeddingResponse:
        """Get embeddings from a model"""
        return await self._aget_embeddings_openai(params=params)


class BaseChatModel(BaseModelhubModel, ABC):
    """
    BaseChatModel: Base class for chat models
    """

    def _pop_custom_parameters(self, parameters: Dict[str, Any]):
        parameters.pop("return_type", None)
        parameters.pop("schema", None)
        return parameters

    async def _achat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> TextGenerationOutput:
        """Chat with a model asynchronously"""
        return await anyio.to_thread.run_sync(self._chat, prompt, parameters)

    @local_model_support
    async def achat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> TextGenerationOutput:
        self._pop_custom_parameters(parameters)
        return await self._achat(prompt=prompt, parameters=parameters)

    async def _abatch_chat(
        self, batch_prompts: List[str], batch_parameters: List[LMParameters] = []
    ) -> List[TextGenerationOutput]:
        """Chat with a model asynchronously"""
        outputs = [None] * len(batch_prompts)

        async def _output(i, prompt, parameters):
            outputs[i] = await self._achat(prompt, parameters)

        async with anyio.create_task_group() as tg:
            for i, (prompt, parameters) in enumerate(
                zip(batch_prompts, batch_parameters)
            ):
                tg.start_soon(_output, i, prompt, parameters)

        return outputs

    @local_model_support
    async def abatch_chat(
        self, batch_prompts: List[str], batch_parameters: List[LMParameters] = []
    ):
        batch_parameters = [
            self._pop_custom_parameters(parameters) for parameters in batch_parameters
        ]
        return await self._abatch_chat(
            batch_prompts=batch_prompts, batch_parameters=batch_parameters
        )

    async def _astream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        """Stream chat with a model asynchronously"""
        stream = await anyio.to_thread.run_sync(self._stream, prompt, parameters)
        for delta in stream:
            yield delta

    @local_model_support
    async def astream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        """Stream chat with a model asynchronously"""
        self._pop_custom_parameters(parameters)
        async for token in self._astream(prompt=prompt, parameters=parameters):
            yield token

    async def _aopenai_chat(self, req: CompletionCreateParams):
        prompt, params = prepare_modelhub_args(req)

        async def stream_generator():
            async for token in self.astream(prompt, params):
                yield s2o(token)

        if req["stream"]:
            return stream_generator()
        else:
            return g2o(await self.achat(prompt, params))

    @local_model_support
    async def aopenai_chat(self, req: CompletionCreateParams):
        return await self._aopenai_chat(req=req)

    def _chat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> TextGenerationOutput:
        """Chat with a model"""
        raise NotImplementedError("chat is not supported for this model")

    def _stream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        yield TextGenerationStreamOutput(
            token=TextGenerationStreamToken(
                text=self._chat(prompt, parameters).generated_text
            )
        )

    def n_tokens(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any] = {},
    ) -> int:
        """Get the number of tokens in a prompt"""
        raise NotImplementedError("n_tokens is not supported for this model")


class BaseLocalChatModel(BaseChatModel):
    model: Any = None
    llm: Any = None
    tokenizer: Any = None

    @local_model_support
    async def achat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: LMParameters = {},
    ) -> Coroutine[Any, Any, TextGenerationOutput]:
        from lmformatenforcer import JsonSchemaParser, RegexParser
        from lmformatenforcer.integrations.transformers import (
            build_transformers_prefix_allowed_tokens_fn,
        )

        if "max_tokens" in parameters:
            parameters["max_new_tokens"] = parameters.pop("max_tokens")
        return_type = parameters.pop("return_type", "text")
        schema = parameters.pop("schema", None)
        logger.info(f"building prefix_allowed_tokens_fn for schema {schema}")
        if return_type != "text" and schema is None:
            raise ValueError("schema is required when return_type is not text")
        if return_type == "text":
            return await self._achat(prompt, parameters)
        if return_type == "json":
            parser = JsonSchemaParser(schema)
        elif return_type == "regex":
            parser = RegexParser(schema)
        else:
            raise ValueError(f"return_type {return_type} is not supported")
        prefix_allowed_tokens_fn = build_transformers_prefix_allowed_tokens_fn(
            self.tokenizer, parser
        )
        logger.info(f"prefix_allowed_tokens_fn built for schema {schema}")
        parameters["prefix_allowed_tokens_fn"] = prefix_allowed_tokens_fn
        res = await self._achat(prompt, parameters)
        return res
