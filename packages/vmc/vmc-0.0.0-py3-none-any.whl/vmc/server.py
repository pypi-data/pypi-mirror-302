import json

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from vmc.exception import exception_handler
from vmc.utils import check_user_auth, get_auth_params
from vmc.models.model_factory import get_model_factory
from vmc.routes import modelhub, openai
from vmc.types.errors import errors as err
from vmc.types.errors.message import ErrorMessage
from vmc.types.errors.status_code import STATUS_CODE as s

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions"""
    return ErrorMessage(
        code=s.BAD_PARAMS, msg=json.dumps(jsonable_encoder(exc.errors()))
    ).r()


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    """Handle exceptions"""
    msg = await exception_handler(exc, {"url": request.url.path})
    return msg.r()


@app.middleware("http")
async def validate_token(request: Request, call_next):
    """Validate token"""
    authorized = check_user_auth(get_auth_params(request))
    if not authorized:
        logger.warning(f"auth failed {get_auth_params(request)}")
        raise err.AuthenticationError()
    return await call_next(request)


app.include_router(openai.router)
app.include_router(modelhub.router)


get_model_factory()
