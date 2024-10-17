from slark import AsyncLark
from modelhub_server.config import get_config

_client: AsyncLark | None = None


def get_lark_client() -> AsyncLark:
    global _client
    if _client is None:
        _client = AsyncLark(webhook=get_config().app.alert_push_url)
    return _client
