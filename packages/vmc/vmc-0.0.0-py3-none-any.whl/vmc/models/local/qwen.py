from vmc.types.chat import (
    TextGenerationStreamOutput,
    TextGenerationDetails,
    TextGenerationOutput,
    LMParameters,
)
from vmc.models._base import BaseChatModel
from typing import Generator, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from vmc.utils.utils import torch_gc


class QwenChatModel(BaseChatModel):
    max_new_tokens: int = 512

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        ).eval()
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True, use_fast=False
        )

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(max_new_tokens=self.max_new_tokens)

    def _model_chat(self, prompt, parameters: LMParameters = {}, stream=False):
        history = parameters.pop("history", [])
        pair_histroy = []
        for i in range(0, len(history), 2):
            pair_histroy.append((history[i]["content"], history[i + 1]["content"]))
        if stream:

            def _stream():
                last_response = ""
                for response in self._model.chat_stream(
                    self._tokenizer, prompt, history=pair_histroy, **parameters
                ):
                    yield TextGenerationStreamOutput(
                        token={"text": response[len(last_response) :]},
                        details=TextGenerationDetails(model=self.config.name),
                    )
                    last_response = response

            torch_gc()
            return _stream()
        else:
            response, new_history = self._model.chat(
                self._tokenizer, prompt, history=pair_histroy, **parameters
            )
            torch_gc()
            return TextGenerationOutput(
                generated_text=response,
                details=TextGenerationDetails(model=self.config.name),
            )

    def _chat(
        self, prompt: str, parameters: LMParameters = {}
    ) -> TextGenerationOutput:
        return self._model_chat(prompt, parameters)

    def _stream(
        self, prompt: str, parameters: LMParameters = {}
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        yield from self._model_chat(prompt, parameters, stream=True)
