from typing import Annotated, Optional

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger

from vmc.models.model_factory import get_model_factory
from vmc.utils import get_auth_params, log_to_db
from vmc.models.local.whisper import BaseAudioModel
from vmc.types.auth import AuthParams
from vmc.types.embedding import EmbeddingCreateParams
from openai.types.audio import TranscriptionCreateParams
from vmc.types.chat.openai_create import RequestParams
from vmc.exception import exception_handler

router = APIRouter()


async def _stream_generator(auth: AuthParams, req: RequestParams):
    try:
        model = await get_model_factory().aget(req["model"])
        res = []
        async for token in await model.aopenai_chat(req):
            res.append(token)
            yield f"data: {token.json()}\n\n"
        log_to_db(auth.user_name, req["model"], req, res)
    except Exception as e:
        msg = await exception_handler(e, {"model": req["model"]})
        yield msg.e()
        return


@router.post("/v1/chat/completions")
async def chat_completion(req: RequestParams, request: Request):
    auth = get_auth_params(request)
    req["stream"] = req.get("stream", False)
    for message in req["messages"]:
        if "function_call" in message and not message["function_call"]:
            message.pop("function_call")

    logger.info(f"[OPENAI] user: {auth.user_name} model: {req['model']}")

    if req["stream"]:
        return StreamingResponse(
            _stream_generator(auth, req),
            media_type="text/event-stream",
            headers={"X-Accel-Buffering": "no"},
        )

    model = await get_model_factory().aget(req["model"])

    res = await model.aopenai_chat(req)
    log_to_db(auth.user_name, req["model"], req, res)
    return res


@router.post("/v1/audio/transcriptions")
async def transciption(
    file: Annotated[UploadFile, File()],
    model: Annotated[str, Form()],
    language: Annotated[Optional[str], Form()] = None,
    temperature: Annotated[Optional[float], Form()] = None,
):
    req = TranscriptionCreateParams(
        file=await file.read(), model=model, language=language, temperature=temperature
    )
    logger.info(f"transcription request: {req['model']}, {file.filename}")
    model: BaseAudioModel = await get_model_factory().aget(model)
    return model.transcribe(req)


@router.post("/v1/embeddings")
async def embeddings(params: EmbeddingCreateParams):
    _param_without_input = {k: v for k, v in params.items() if k != "input"}
    logger.info(f"[OPENAI EMBEDDING] {_param_without_input}")
    model = await get_model_factory().aget(params["model"])
    return await model.aget_embeddings_openai(params)


@router.get("/v1/models")
async def model():
    return {
        "object": "list",
        "data": [
            {
                "id": model_name,
                "object": "model",
                "created": 1686935002,
                "owned_by": "modelhub",
            }
            for model_name in get_model_factory().models.keys()
        ],
    }
