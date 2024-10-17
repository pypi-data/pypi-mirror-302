from vmc.types.chat import (
    TextGenerationOutput,
    TextGenerationDetails,
    BaseMessage,
)
from vmc.models._base import BaseChatModel

from typing import Optional, Dict, Any, List, Union
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json


class DeepseekBaseModel(BaseChatModel):
    model_id: str
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            use_flash_attention_2=True,
            torch_dtype=torch.bfloat16,
        ).cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        # os.environ["CUDA_VISIBLE_DEVICES"] = ""
        self.model.eval()

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=128,
        )

    def _chat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any] = {},
    ) -> TextGenerationOutput:
        parameters.pop("history")
        if isinstance(prompt, list):
            prompt = prompt[-1].content
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        parameters = self.default_parameters | parameters
        outputs = self.model.generate(**inputs, **parameters)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )


class DeepseekModel(BaseChatModel):
    model_id: str
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            use_flash_attention_2=True,
            torch_dtype=torch.bfloat16,
        ).cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        self.model.eval()

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(
            max_new_tokens=512,
            do_sample=False,
            top_k=50,
            top_p=0.95,
            num_return_sequences=1,
            eos_token_id=32021,
        )

    def _chat(
        self,
        prompt: Union[str, List[BaseMessage]],
        parameters: Dict[str, Any] = {},
    ) -> TextGenerationOutput:
        if isinstance(prompt, str):
            messages = parameters.pop("history", []) + [
                {"role": "user", "content": prompt}
            ]
        else:
            messages = [
                m.model_dump() if isinstance(m, BaseMessage) else m for m in prompt
            ]
            parameters.pop("history", [])
        inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to(
            self.model.device
        )
        parameters = self.default_parameters | parameters
        outputs = self.model.generate(inputs, **parameters)
        response = self.tokenizer.decode(
            outputs[0][len(inputs[0]) :], skip_special_tokens=True
        )

        if isinstance(response, dict):
            response = json.dumps(response, ensure_ascii=False)
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )
