from typing import Dict, List, Optional, Union, Literal

from openai.types.chat import (
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
    completion_create_params,
)
from pydantic import BaseModel
from typing_extensions import NotRequired, TypedDict

from .message import BaseMessage


class BaseParameters(TypedDict):
    history: NotRequired[List[BaseMessage]]
    return_type: NotRequired[Literal["text", "json", "regex"]]
    schema: NotRequired[str]


class OpenAIParameters(BaseParameters):
    frequency_penalty: NotRequired[float]
    function_call: NotRequired[completion_create_params.FunctionCall]
    functions: NotRequired[List[completion_create_params.Function]]
    logit_bias: NotRequired[Dict[str, int]]
    max_tokens: NotRequired[int]
    n: NotRequired[int]
    presence_penalty: NotRequired[float]
    response_format: NotRequired[completion_create_params.ResponseFormat]
    seed: NotRequired[int]
    stop: NotRequired[Union[Optional[str], List[str]]]
    temperature: NotRequired[float]
    tool_choice: NotRequired[ChatCompletionToolChoiceOptionParam]
    tools: NotRequired[List[ChatCompletionToolParam]]
    top_p: NotRequired[float]
    user: NotRequired[str]
    timeout: NotRequired[float]


LMParameters = dict


class ChatParams(BaseModel):
    """ChatParams: Parameters for chat"""

    prompt: Union[str, List[BaseMessage]]
    model: str
    stream: bool = False
    parameters: LMParameters = {}


class BatchChatParams(BaseModel):
    batch_prompts: List[str]
    model: str
    batch_parameters: List[LMParameters] = []