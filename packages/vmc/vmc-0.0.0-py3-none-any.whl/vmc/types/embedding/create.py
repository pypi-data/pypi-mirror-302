from typing import Any, List, Dict, Union

from typing_extensions import TypedDict, Required, Literal

from pydantic import BaseModel


class EmbeddingParams(BaseModel):
    """EmbeddingParams: Parameters for embedding"""

    prompt: str | List[str]
    model: str
    parameters: Dict[str, Any] = {}


class EmbeddingCreateParams(TypedDict, total=False):
    input: Required[Union[str, List[str], List[int], List[List[int]]]]
    model: Required[Union[str, Literal["text-embedding-ada-002"]]]
    encoding_format: Literal["float", "base64"]
    user: str
    dimensions: int
