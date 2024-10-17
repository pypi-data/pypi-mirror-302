import hashlib
import subprocess

import numpy as np
from typing import Any, Dict

from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from modelhub_server.types.chat import (
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationDetails,
    TextGenerationStreamToken,
    ToolCallOutput,
)


def o2g(c: ChatCompletion) -> TextGenerationOutput:
    """Transform OpenAI Completion to TextGeneration"""
    tool_calls = c.choices[0].message.tool_calls
    return TextGenerationOutput(
        generated_text=c.choices[0].message.content or "",
        tool_calls=[ToolCallOutput.model_validate(tc.model_dump()) for tc in tool_calls]
        if tool_calls
        else None,
        details=TextGenerationDetails(
            finish_reason=c.choices[0].finish_reason,
            created=c.created,
            model=c.model,
            prompt_tokens=c.usage.prompt_tokens,
            generated_tokens=c.usage.completion_tokens,
        ),
    )


def g2o(g: TextGenerationOutput) -> ChatCompletion:
    """Transform TextGeneration to OpenAI Completion"""
    return ChatCompletion(
        id="",
        choices=[
            {
                "finish_reason": g.details.finish_reason,
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": g.generated_text,
                    "tool_calls": [tc.model_dump() for tc in g.tool_calls]
                    if g.tool_calls
                    else None,
                },
            }
        ],
        created=g.details.created,
        model=g.details.model,
        object="chat.completion",
        usage={
            "prompt_tokens": g.details.prompt_tokens,
            "completion_tokens": g.details.generated_tokens,
            "total_tokens": g.details.prompt_tokens + g.details.generated_tokens,
        },
    )


def o2s(c: ChatCompletionChunk) -> TextGenerationStreamOutput:
    """Transform OpenAI CompletionChunk to TextGeneration"""
    tool_calls = c.choices[0].delta.tool_calls
    return TextGenerationStreamOutput(
        token=TextGenerationStreamToken(text=c.choices[0].delta.content or ""),
        tool_calls=[ToolCallOutput.model_validate(tc.model_dump()) for tc in tool_calls]
        if tool_calls
        else None,
        details=TextGenerationDetails(
            finish_reason=c.choices[0].finish_reason, created=c.created, model=c.model
        ),
    )


def s2o(s: TextGenerationStreamOutput) -> ChatCompletionChunk:
    """Transform TextGeneration to OpenAI CompletionChunk"""
    return ChatCompletionChunk(
        id="0",
        choices=[
            {
                "delta": {
                    "content": s.token.text,
                    "role": "assistant",
                    "tool_calls": [tc.model_dump() for tc in s.tool_calls]
                    if s.tool_calls
                    else None,
                },
                "index": 0,
                "finish_reason": s.details.finish_reason,
            }
        ],
        created=s.details.created,
        model=s.details.model,
        object="chat.completion.chunk",
    )


def prepare_modelhub_args(req: CompletionCreateParams) -> Dict[str, Any]:
    params = {"history": []}
    if "temperature" in req:
        params["temperature"] = req["temperature"]
    if "top_p" in req:
        params["top_p"] = req["top_p"]
    if "max_tokens" in req:
        params["max_tokens"] = req["max_tokens"]
    if "presence_penalty" in req:
        params["presence_penalty"] = req["presence_penalty"]
    if "frequency_penalty" in req:
        params["frequency_penalty"] = req["frequency_penalty"]
    if "tools" in req:
        params["tools"] = req["tools"]
    if "tool_choice" in req:
        params["tool_choice"] = req["tool_choice"]
    return req["messages"], params


def get_gpu_free_memory():
    cmd = "nvidia-smi --query-gpu=memory.free --format=csv,nounits,noheader"
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    memory = [int(x) for x in output.strip().split("\n")]
    return memory


def get_freer_gpu(top_k=1, exclude_gpus=[]):
    gpu_memory = get_gpu_free_memory()
    for i in exclude_gpus:
        gpu_memory[i] = -1
    return sorted(np.argsort(gpu_memory)[::-1][:top_k])


def torch_gc(device: int = 0):
    import torch
    import gc

    if torch.cuda.is_available():
        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def hash_password(password: str):
    """
    Hash a password"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def find_available_port():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port
