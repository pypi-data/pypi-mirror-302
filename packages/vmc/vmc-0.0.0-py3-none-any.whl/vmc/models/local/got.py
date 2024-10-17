from vmc.types.chat import (
    TextGenerationDetails,
    TextGenerationOutput,
    LMParameters,
)
from vmc.models._base import BaseLocalChatModel
from typing import Dict, Any
from transformers import AutoTokenizer, AutoModel
import re
import os
from vmc.utils.storage import get_file_path


class GOTChatModel(BaseLocalChatModel):
    max_new_tokens: int = 512

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            self.model_id,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            device_map="cuda",
            use_safetensors=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        self.model = self.model.eval().cuda()

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return dict(max_new_tokens=self.max_new_tokens)

    def _prepare_chat_inputs(self, prompt: str, parameters: dict) -> dict:
        inputs = {}
        match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", prompt)
        if not match:
            raise ValueError("Input must be an image")
        possible_keys = ["ocr_type", "ocr_box", "ocr_color"]
        for k in possible_keys:
            if k in parameters:
                inputs[k] = parameters[k]
        inputs["tokenizer"] = self.tokenizer
        image_file = get_file_path(match.group(2))
        if not image_file or not os.path.exists(image_file):
            raise ValueError(f"Image {image_file} not found")
        inputs["image_file"] = image_file
        return inputs

    def _chat(self, prompt: str, parameters: LMParameters = {}) -> TextGenerationOutput:
        chat_inputs = self._prepare_chat_inputs(prompt, parameters)
        res = self.model.chat(**chat_inputs)
        return TextGenerationOutput(generated_text=res, details=TextGenerationDetails())
