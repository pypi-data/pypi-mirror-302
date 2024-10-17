from typing import Any, Dict
from pydantic import BaseModel


class TokensParams(BaseModel):
    """TokensParams: Parameters for tokens"""

    prompt: str
    model: str
    parameters: Dict[str, Any] = {}
