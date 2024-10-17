import datetime
import uuid
from typing import List

from fastapi import Request
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from pymongo.collection import Collection

from modelhub_server.types.chat import ChatParams
from modelhub_server.config import get_config
from modelhub_server.lib.auth import get_auth_params
from modelhub_server.lib.db import get_mongo_db
from loguru import logger


def log_to_db(
    user_id: str,
    model_id: str,
    req: CompletionCreateParams,
    res: ChatCompletion | List[ChatCompletionChunk],
    db: Collection | None = None,
):
    if not get_config().app.log_requests:
        return None
    try:
        if not db:
            db = get_mongo_db()[get_config().db.openai_collection]
        if isinstance(res, ChatCompletion):
            res = res.dict()
        elif isinstance(res, list):
            res = [c.dict() for c in res]
        result = db.insert_one(
            {
                "user_id": user_id,
                "model_id": model_id,
                "req": req,
                "res": res,
                "created": datetime.datetime.now(),
            }
        )
    except Exception as e:
        logger.error(f"Failed to save message: {e}")
        return None
    return result.inserted_id


def log_to_db_modelhub(
    req: Request,
    params: ChatParams,
    response,
    db: Collection | None = None,
):
    if not get_config().app.log_requests:
        return None
    try:
        if not db:
            db = get_mongo_db()[get_config().db.messages_collection]
        auth = get_auth_params(req)
        if isinstance(params.prompt, list):
            prompt = [p.model_dump() for p in params.prompt]
        else:
            prompt = params.prompt
        result = db.insert_one(
            {
                "message_id": str(uuid.uuid4()),
                "user_id": auth.user_name,
                "model": params.model,
                "prompt": prompt,
                "stream": params.stream,
                "parameters": params.parameters,
                "response": response,
                "created_time": datetime.datetime.now(),
            }
        )
    except Exception as e:
        logger.error(f"Failed to save message: {e}")
        return None
    return result.inserted_id
