import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger
from openai.types.audio.transcription_create_params import TranscriptionCreateParams

from vmc.types.token import NTokensOutput
from vmc.types.models import ModelInfoOutput
from vmc.types.chat import TextGenerationDetails

from vmc.models.local.whisper import BaseAudioModel
from vmc.models.model_factory import get_model_factory
from vmc.utils import get_auth_params
from vmc.utils import log_to_db_modelhub as log_request
from vmc.utils.storage import store_file
from vmc.models._base import BaseCrossEncoderModel
from vmc.types.chat import ChatParams, BatchChatParams
from vmc.types.embedding import EmbeddingParams
from vmc.types.rerank import CrossEncodingParams
from vmc.types.errors import errors as err
from vmc.exception import exception_handler
from vmc.types.image.upload import ImageUploadOutput

router = APIRouter()


async def _stream_generator(params: ChatParams, request: Request):
    try:
        model = await get_model_factory().aget(params.model)

        tokens = []
        async for token in model.astream(params.prompt, params.parameters):
            yield token.e()
            tokens.append(token.dict())
    except Exception as e:
        msg = await exception_handler(e, {"model": params.model})
        yield msg.e()
        return
    log_request(request, params, tokens)


@router.post("/batch_chat")
async def batch_chat(params: BatchChatParams, request: Request):
    auth = get_auth_params(request)
    logger.info(f"[MODELHUB] user: {auth.user_name} model: {params.model}")
    model = await get_model_factory().aget(params.model)

    batch_parameters = params.batch_parameters
    if not batch_parameters:
        batch_parameters = [{}]
    if len(batch_parameters) == 1:
        batch_parameters = batch_parameters * len(params.batch_prompts)
    elif len(batch_parameters) != len(params.batch_prompts):
        raise err.BadParamsError(
            msg="batch_parameters and batch_prompt must have the same length"
        )

    outputs = await model.abatch_chat(params.batch_prompts, batch_parameters)
    return outputs


@router.post("/chat")
async def chat(params: ChatParams, request: Request):
    """Chat with a model"""
    auth = get_auth_params(request)
    logger.info(f"[MODELHUB] user: {auth.user_name} model: {params.model}")

    if params.stream:
        return StreamingResponse(
            _stream_generator(params, request),
            media_type="text/event-stream",
            headers={"X-Accel-Buffering": "no"},
        )

    start_time = datetime.datetime.now()

    model = await get_model_factory().aget(params.model)
    output = await model.achat(params.prompt, params.parameters)
    request_time = datetime.datetime.now() - start_time
    if not output.details:
        output.details = TextGenerationDetails()
    output.details.request_time = request_time.total_seconds()
    log_request(request, params, output.dict())
    return output


@router.post("/embedding")
async def embedding(params: EmbeddingParams, request: Request):
    """Get embeddings from a model"""
    auth = get_auth_params(request)
    logger.info(f"[EMBEDDING] user: {auth.user_name} model: {params.model}")

    model = await get_model_factory().aget(params.model)
    return await model.aget_embeddings(params.prompt, params.parameters)


@router.post("/cross_embedding")
async def cross_embedding(params: CrossEncodingParams):
    """Get embeddings from a model"""
    logger.info(f"[CROSS EMBEDDING] model: {params.model}")
    model: BaseCrossEncoderModel = await get_model_factory().aget(params.model)
    return await model.apredict(params.sentences, params.parameters)


@router.get("/models")
async def get_models():
    return ModelInfoOutput(models=get_model_factory().models)


@router.post("/tokens")
async def tokens(params: ChatParams):
    """Get tokens from a model"""
    model = await get_model_factory().aget(params.model)

    n_tokens = model.n_tokens(params.prompt, params.parameters)
    return NTokensOutput(n_tokens=n_tokens)


@router.post("/audio/transcriptions")
async def transciption(
    file: Annotated[UploadFile, File()],
    model: Annotated[str, Form()],
    language: Annotated[Optional[str], Form()] = None,
    temperature: Annotated[Optional[float], Form()] = None,
):
    req = TranscriptionCreateParams(
        file=await store_file(file, return_path=True),
        model=model,
        language=language,
        temperature=temperature,
    )
    logger.info(f"[Transcription] {req['model']}, {file.filename}")
    model: BaseAudioModel = await get_model_factory().aget(req["model"])
    return model.transcribe(req)


@router.post("/image/upload")
async def image_upload(file: UploadFile = File(...)):
    return ImageUploadOutput(id=await store_file(file))


@router.get("/ping")
async def ping():
    return {"code": 200, "msg": "pong"}
