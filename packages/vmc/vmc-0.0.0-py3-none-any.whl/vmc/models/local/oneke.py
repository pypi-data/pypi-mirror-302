from vmc.types.chat import TextGenerationOutput, TextGenerationDetails
from vmc.models._base import BaseLocalChatModel

from loguru import logger
from typing import Dict, Any


class OneKEModel(BaseLocalChatModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from vllm import LLM

        logger.info(f"Loading {self.__class__.__name__} model")
        self.llm = LLM(self.model_id, tensor_parallel_size=2)

    def _chat(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationOutput:
        from vllm import SamplingParams

        _ = parameters.pop("history", None)
        system_prompt = "<<SYS>>\nYou are a helpful assistant. 你是一个乐于助人的助手。\n<</SYS>>\n\n"
        sintruct = "[INST] " + system_prompt + prompt + "[/INST]"
        parameters = {**self.config.default_params, **parameters}
        text = (
            self.llm.generate(sintruct, SamplingParams(**parameters))[0]
            .outputs[0]
            .text.strip()
        )
        return TextGenerationOutput(
            generated_text=text, details=TextGenerationDetails(model=self.config.name)
        )
