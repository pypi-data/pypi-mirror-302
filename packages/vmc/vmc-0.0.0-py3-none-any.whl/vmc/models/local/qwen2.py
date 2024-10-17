from vmc.types.chat import TextGenerationOutput, TextGenerationDetails
from vmc.models._base import BaseLocalChatModel

from typing import Dict, Any


class Qwen2Model(BaseLocalChatModel):
    gpu_memory_utilization = 0.8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from vllm import LLM
        from transformers import AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.llm = LLM(
            self.model_id,
            tensor_parallel_size=self.config.max_gpu_usage,
            max_model_len=self.config.context_window,
            gpu_memory_utilization=self.gpu_memory_utilization,
            enforce_eager=True,
        )

    def _chat(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationOutput:
        from vllm import SamplingParams

        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        tokens = self.tokenizer(text)
        if len(tokens["input_ids"]) > 4096:
            raise ValueError(f"Input size {len(tokens['input_ids'])} is too large")
        output = (
            self.llm.generate(
                text,
                SamplingParams(**parameters),
            )[0]
            .outputs[0]
            .text.strip()
        )
        return TextGenerationOutput(
            generated_text=output,
            details=TextGenerationDetails(
                model=self.config.name,
                prompt_tokens=len(tokens["input_ids"]),
            ),
        )
