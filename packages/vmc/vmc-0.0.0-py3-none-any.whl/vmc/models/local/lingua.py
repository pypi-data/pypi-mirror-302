from typing import Any, Dict
from vmc.types.chat import TextGenerationOutput, TextGenerationDetails
from vmc.models._base import BaseLocalChatModel


class LLMLingua(BaseLocalChatModel):
    def __init__(self, **kwargs):
        from llmlingua import PromptCompressor

        super().__init__(**kwargs)
        self.model = PromptCompressor(self.model_id)

    def _chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        context = parameters.pop("history", []) + [prompt]
        response = self.model.compress_prompt(context, **parameters)[
            "compressed_prompt"
        ]
        return TextGenerationOutput(
            generated_text=response,
            details=TextGenerationDetails(model=self.config.name),
        )
