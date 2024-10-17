from vmc.types.audio import Transcription
from openai.types.audio.transcription_create_params import TranscriptionCreateParams
from .._base import BaseAudioModel


class FunASR(BaseAudioModel):
    pipeline: object = None

    def __init__(self, **kwargs):
        from funasr import AutoModel
        
        super().__init__(**kwargs)
        self.pipeline = AutoModel(
            model=self.model_id, vad_model="fsmn-vad", punc_model="ct-punc-c"
        )

    def transcribe(self, req: TranscriptionCreateParams) -> Transcription:
        return Transcription(text=self.pipeline(req["file"])[0]["text_postprocessed"])
