from vmc.types.chat import (
    TextGenerationOutput,
    TextGenerationDetails,
)
from .._base import BaseChatModel
from typing import Optional, Dict, Any
import torch


class XVerseModel(BaseChatModel):
    model_id: str
    temperature: float = 0.01
    top_p: float = 0.9
    is_multi_gpu: bool = False
    max_tokens: int = 262144
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from transformers import AutoTokenizer, AutoModelForCausalLM
        from transformers.generation.utils import GenerationConfig

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        self.model.generation_config = GenerationConfig.from_pretrained(self.model_id)
        self.model.generation_config.use_cache = False
        self.model = self.model.eval()
        self.model.eval()

    def n_tokens(self, prompt: str, parameters: Dict[str, Any] = {}) -> int:
        encoding = self.tokenizer.encode(prompt, **parameters)
        return len(encoding)

    def _generate(self, prompt: str, parameters: Dict[str, Any] = {}) -> str:
        return parameters.pop("history", []) + [{"role": "user", "content": prompt}]

    def _chat(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationOutput:
        inputs = self._generate(prompt, parameters)
        response = self.model.chat(self.tokenizer, inputs, **parameters)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )
