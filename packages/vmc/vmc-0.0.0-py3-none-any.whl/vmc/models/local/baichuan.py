from typing import Any, Dict, Generator, List, Union

import torch

from vmc.types.chat import (
    TextGenerationDetails,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    BaseMessage,
)
from vmc.utils.utils import torch_gc
from vmc.models._base import BaseLocalChatModel


def build_chat_input(model, tokenizer, messages: List[dict], max_new_tokens: int = 0):
    def _parse_messages(messages, split_role="user"):
        system, rounds = "", []
        round = []
        for i, message in enumerate(messages):
            if message["role"] == "system":
                assert i == 0
                system = message["content"]
                continue
            if message["role"] == split_role and round:
                rounds.append(round)
                round = []
            round.append(message)
        if round:
            rounds.append(round)
        return system, rounds

    max_new_tokens = max_new_tokens or model.generation_config.max_new_tokens
    max_input_tokens = model.config.model_max_length - max_new_tokens
    system, rounds = _parse_messages(messages, split_role="user")
    system_tokens = tokenizer.encode(system)
    max_history_tokens = max_input_tokens - len(system_tokens)

    history_tokens = []
    for round in rounds[::-1]:
        round_tokens = []
        for message in round:
            if message["role"] == "user":
                round_tokens.append(model.generation_config.user_token_id)
            else:
                round_tokens.append(model.generation_config.assistant_token_id)
            round_tokens.extend(tokenizer.encode(message["content"]))
        if (
            len(history_tokens) == 0
            or len(history_tokens) + len(round_tokens) <= max_history_tokens
        ):
            history_tokens = round_tokens + history_tokens  # concat left
            if len(history_tokens) < max_history_tokens:
                continue
        break

    input_tokens = system_tokens + history_tokens
    if messages[-1]["role"] != "assistant":
        input_tokens.append(model.generation_config.assistant_token_id)
    input_tokens = input_tokens[-max_input_tokens:]  # truncate left
    return torch.LongTensor([input_tokens]).to(model.device)


class Baichuan2Local(BaseLocalChatModel):
    default_generate_parameters: Dict[str, Any] = {
        "max_new_tokens": 256,
        "temperature": 0.01,
        "do_sample": True,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from transformers import AutoModelForCausalLM, AutoTokenizer
        from transformers.generation.utils import GenerationConfig

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            use_fast=False,
        )
        self.model.generation_config = GenerationConfig.from_pretrained(self.model_id)

    def n_tokens(self, prompt: str, parameters: Dict[str, Any] = {}) -> int:
        encoding = self.tokenizer.encode(prompt, **parameters)
        return len(encoding)

    def _prepare_chat_args(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
        stream: bool = False,
    ):
        parameters = {**self.default_generate_parameters, **parameters}
        if isinstance(prompt, str):
            messages = parameters.pop("history", []) + [
                {"role": "user", "content": prompt}
            ]
        else:
            messages = [
                m.model_dump() if isinstance(m, BaseMessage) else m for m in prompt
            ]
            parameters.pop("history", [])
        input_ids = build_chat_input(
            self.model, self.tokenizer, messages, parameters.get("max_new_tokens", 0)
        )
        if stream:
            return {
                "tokenizer": self.tokenizer,
                "messages": messages,
                **parameters,
                "stream": True,
            }
        else:
            return {"input_ids": input_ids, **parameters}

    def _generate(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
        stream=False,
    ):
        args = self._prepare_chat_args(prompt, parameters, stream=stream)
        if stream:

            def _stream():
                for response in self.model.chat(**args):
                    yield response
                    torch_gc()

            return _stream()
        else:
            outputs = self.model.generate(**args)
            response = self.tokenizer.decode(
                outputs[0][len(args["input_ids"][0]) :], skip_special_tokens=True
            )
            return response

    def _chat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> TextGenerationOutput:
        response = self._generate(prompt, parameters)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )

    def _stream(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any],
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        generated_text = ""
        for response in self._generate(prompt, parameters, stream=True):
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(text=response[len(generated_text) :]),
                details=TextGenerationDetails(model=self.config.name),
            )
            generated_text = response
