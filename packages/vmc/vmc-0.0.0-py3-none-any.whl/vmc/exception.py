import traceback

import openai
import zhipuai
from loguru import logger

from vmc.utils.lark import get_lark_client
from vmc.utils.time import get_current_date_formatted
from vmc.utils.string import trunctuate_string
from vmc.types import errors as err
from vmc.types.errors import ErrorMessage
from vmc.types.errors.status_code import STATUS_CODE as s

__exception_map = {
    openai.APITimeoutError: s.API_TIMEOUT,
    openai.APIConnectionError: s.API_CONNECTION_ERROR,
    openai.BadRequestError: s.BAD_PARAMS,
    openai.AuthenticationError: s.UNAUTHORIZED,
    zhipuai.APIAuthenticationError: s.UNAUTHORIZED,
    openai.NotFoundError: s.MODEL_NOT_FOUND,
    openai.RateLimitError: s.API_RATE_LIMIT,
    err.APITimeoutError: s.API_TIMEOUT,
    err.APIConnectionError: s.API_CONNECTION_ERROR,
    err.AuthenticationError: s.UNAUTHORIZED,
    err.ModelNotFoundError: s.MODEL_NOT_FOUND,
    err.RateLimitError: s.API_RATE_LIMIT,
    err.ModelhubException: s.INTERNAL_ERROR,
    err.ManagerNotLoadedError: s.MANAGER_NOT_LOADED,
}


def _replace_markdown_image(text: str):
    import re

    return re.sub(r"!\[(.*?)\]\((.*?)\)", r"Image: \1", text)


async def exception_handler(exec: Exception, context: dict | None = None):
    code = __exception_map.get(exec.__class__, s.INTERNAL_ERROR)
    tb = traceback.format_exc()
    if hasattr(exec, "context"):
        context = {**context, **exec.context}
    msg = f"{str(exec)}\n{context}"
    logger.exception(msg)
    try:
        await get_lark_client().webhook.post_error_card(
            _replace_markdown_image(trunctuate_string(msg, 500)),
            _replace_markdown_image(tb),
            exec.__class__.__name__,
            f"{context.get('model', 'Unkonwn')}, {get_current_date_formatted()}",
        )
    except Exception as e:
        logger.warning(f"Failed to send error message to lark: {e}")
    return ErrorMessage(code=code, msg=str(exec))
