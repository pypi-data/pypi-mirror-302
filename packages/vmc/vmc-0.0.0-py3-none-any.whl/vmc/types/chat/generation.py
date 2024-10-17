from typing import List, Literal, Optional


from .._base import BaseModel, BaseOutput


class TextGenerationStreamToken(BaseModel):
    text: str


class TextGenerationDetails(BaseModel):
    finish_reason: (
        Literal["stop", "length", "tool_calls", "content_filter", "function_call"]
        | None
    ) = "stop"
    created: Optional[int] = None
    model: Optional[str] = None
    request_time: Optional[float] = None
    prompt_tokens: Optional[int] = None
    generated_tokens: Optional[int] = None


class FunctionOutput(BaseModel):
    arguments: str
    name: str


class ToolCallOutput(BaseModel):
    id: str
    function: FunctionOutput
    type: Literal["function"] | str = "function"


class TextGenerationStreamOutput(BaseOutput):
    token: TextGenerationStreamToken
    tool_calls: Optional[List[ToolCallOutput]] = None
    details: Optional[TextGenerationDetails] = None


class TextGenerationOutput(BaseOutput):
    generated_text: str
    tool_calls: Optional[List[ToolCallOutput]] = None
    details: Optional[TextGenerationDetails] = None
