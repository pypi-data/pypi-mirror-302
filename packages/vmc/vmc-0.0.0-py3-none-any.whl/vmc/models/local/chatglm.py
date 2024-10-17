import json
from typing import Any, Dict, Generator, List, Union

from transformers import AutoModel, AutoTokenizer

from vmc.types.chat import (
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationDetails,
    BaseMessage,
)
from vmc.models._base import BaseLocalChatModel


class ChatGLMLocal(BaseLocalChatModel):
    temperature: float = 0.01
    top_p: float = 0.9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = AutoModel.from_pretrained(
            self.model_id, trust_remote_code=True, device_map="auto"
        ).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )

    def n_tokens(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any] = {},
    ) -> int:
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id, trust_remote_code=True
            )
        return len(self.tokenizer.encode(prompt, **parameters))

    def _generate(
        self,
        prompt: Union[str, List[BaseMessage]],
        history: list[dict],
        stream=False,
        **parameters,
    ):
        if isinstance(prompt, str):
            inputs = self.tokenizer.build_chat_input(
                prompt, history=history, role="user"
            ).to(self.model.device)
        else:
            prompt = [m.dict() for m in prompt]
            inputs = self.tokenizer.build_chat_input(
                prompt[-1]["content"],
                role=prompt[-1]["role"],
                history=prompt[:-1],
            ).to(self.model.device)
        eos_token_id = [
            self.tokenizer.eos_token_id,
            self.tokenizer.get_command("<|user|>"),
            self.tokenizer.get_command("<|observation|>"),
        ]

        n_tokens = len(inputs["input_ids"][0])
        if self.config.max_tokens > 0 and n_tokens > self.config.max_tokens:
            raise ValueError(
                f"Input length {n_tokens} exceeds maximum length {self.max_tokens}"
            )

        def _stream():
            response = ""
            for res_delta, chat_history in self.model.stream_chat(
                self.tokenizer,
                prompt,
                history=history,
                **parameters,
            ):
                yield res_delta[len(response) :], chat_history
                response = res_delta

        if not stream:
            outputs = self.model.generate(
                **inputs, eos_token_id=eos_token_id, **parameters
            )
            outputs = outputs.tolist()[0][n_tokens:-1]
            response = self.tokenizer.decode(outputs)
            return response, history + [{"role": "assistant", "content": response}]
        else:
            return _stream()

    def _chat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> TextGenerationOutput:
        response, new_history = self._generate(prompt, **parameters)
        if isinstance(response, dict):
            response = json.dumps(response, ensure_ascii=False)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )

    def _stream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        for delta, _ in self._generate(prompt, stream=True, **parameters):
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(text=delta),
                details=TextGenerationDetails(model=self.config.name),
            )
