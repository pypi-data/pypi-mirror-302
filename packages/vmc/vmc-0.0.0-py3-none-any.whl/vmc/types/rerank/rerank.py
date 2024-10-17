from typing import List

from .._base import BaseOutput


class CrossEncoderOutput(BaseOutput):
    scores: List[float]
