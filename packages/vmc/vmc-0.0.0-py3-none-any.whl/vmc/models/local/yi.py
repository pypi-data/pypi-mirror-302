from vmc.types.chat import (
    TextGenerationOutput,
    TextGenerationDetails,
)
from vmc.models._base import BaseChatModel
from typing import Optional, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class YiChatModel(BaseChatModel):
    model_id: str
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None
    max_new_tokens: int = 512

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True, use_fast=False
        )
        self.model.eval()

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(max_new_tokens=self.max_new_tokens)

    def _chat(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationOutput:
        messages = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        input_ids = self.tokenizer.apply_chat_template(
            conversation=messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to("cuda")
        parameters = self.default_parameters | parameters
        outputs = self.model.generate(input_ids, **parameters)
        response = self.tokenizer.decode(
            outputs[0][input_ids.shape[1] :], skip_special_tokens=True
        )
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )


class YiBaseModel(BaseChatModel):
    model_id: str
    max_new_tokens: int = 512
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            use_flash_attention_2=True,
            # device_map="auto",
            torch_dtype=torch.bfloat16,
        ).cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        self.model.eval()

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(max_new_tokens=self.max_new_tokens)

    def _chat(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationOutput:
        parameters.pop("history")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        parameters = self.default_parameters | parameters
        outputs = self.model.generate(inputs.input_ids.to("cuda"), **parameters)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(
                model=self.config.name,
                prompt_tokens=len(inputs.input_ids[0]),
            ),
        )
