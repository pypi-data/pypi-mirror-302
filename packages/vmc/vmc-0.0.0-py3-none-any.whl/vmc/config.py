import os
from typing import Any, Dict, Literal, Optional
import pathlib

from loguru import logger
from pydantic.v1 import BaseModel


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8888
    workers: int = 1
    upload_dir: str = "/uploads"
    weights_dir: str = ""
    gpus_per_worker: int = 3
    init_user: str = ""
    init_pass: str = ""

    manager_port: int = 7861
    manager_host: str = "127.0.0.1"
    exclude_gpus: list[int] = []
    alert_push_url: str | None = None
    check_auth: bool = True
    log_requests: bool = True
    init_model_id: str | None = None


class ModelPricing(BaseModel):
    currency: str = "USD"
    input: str = ""
    output: str = ""


class ModelConfig(BaseModel):
    name: str
    class_name: str
    init_kwargs: dict[str, Any] | None = None
    default_params: dict[str, Any] | None = None
    types: list[Literal["chat", "embedding", "audio", "reranker"]] = ["chat"]
    pricing: ModelPricing | None = None
    context_window: int | None = None
    output_dimension: int | None = None
    max_tokens: int | None = None
    description: str | None = None
    knowledge_date: str | None = None
    port: int | None = None
    max_gpu_usage: int = 1
    is_local: bool = False

    def dump(self):
        d = self.dict()
        d.pop("init_kwargs")
        return d

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.max_tokens is None and self.context_window is not None:
            self.max_tokens = self.context_window
        if self.default_params is None:
            self.default_params = {}


class ProviderConfig(BaseModel):
    provider_name: str = "unknown"
    model_page: str = ""
    document_page: str = ""
    credentials: list[dict] | None = None
    models: list[ModelConfig] | None = None
    is_local: bool = False

    @classmethod
    def from_yaml(cls, path: str):
        import yaml

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            obj = cls(**yaml.safe_load(f))
            if "local" in obj.provider_name.lower():
                obj.is_local = True
                for model in obj.models:
                    model.is_local = True
            return obj


class DBConfig(BaseModel):
    mongo_url: str
    mongo_db: str
    messages_collection: str = "messages"
    openai_collection: str = "openai"
    users_collection: str = "users"


class DashboardConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 7860
    user: str
    password: str


class LoggerConfig(BaseModel):
    level: str = "INFO"
    dir: str = "/tmp/log/modelhub/server.log"


class Config(BaseModel):
    logger: LoggerConfig
    """日志配置"""
    env: Optional[Dict[str, str]] = {}
    """环境变量"""
    db: DBConfig
    """数据库配置"""
    app: AppConfig
    """应用配置"""
    providers: list[str | ProviderConfig]
    """模型提供商配置"""
    dashboard: Optional[DashboardConfig] = None
    """dashboard配置"""

    config_path: str | None = None
    """不需要在yaml文件中配置, 由from_yaml方法设置"""

    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        for k, v in self.env.items():
            if k not in self:
                os.environ[k] = v
        for i in range(len(self.providers)):
            if isinstance(self.providers[i], str):
                """如果是字符串，表示是一个yaml文件路径，需要加载yaml文件"""
                path = pathlib.Path(config_path).parent / self.providers[i]
                provider = ProviderConfig.from_yaml(path.as_posix() + ".yaml")
                self.providers[i] = provider
                for model in provider.models:
                    """将本地模型model_id转换为绝对路径"""
                    if model.is_local:
                        model.init_kwargs["model_id"] = os.path.join(
                            self.app.weights_dir, model.init_kwargs["model_id"]
                        )

    @classmethod
    def from_yaml(cls, path: str):
        import yaml

        with open(path, "r", encoding="utf-8") as f:
            obj = cls(config_path=path, **yaml.safe_load(f))
            if "LOG_REQUESTS" in os.environ:
                obj.app.log_requests = os.environ.get("LOG_REQUESTS") == "true"
            if "CHECK_AUTH" in os.environ:
                obj.app.check_auth = os.environ.get("CHECK_AUTH") == "true"
            obj.app.init_model_id = os.environ.get("MODEL_ID", obj.app.init_model_id)
            obj.config_path = os.path.abspath(path)
            return obj


_config = None


def get_config(config_path: str | None = None) -> Config:
    if config_path is None:
        config_path = os.environ.get("CONFIG_PATH", "config.yaml")
    global _config
    if _config is None:
        try:
            _config = Config.from_yaml(config_path)
        except FileNotFoundError as e:
            logger.error(f"Failed to load config from {config_path}: {e}")
            exit(1)
        logger.add(_config.logger.dir, level=_config.logger.level)
        logger.info(f"Loaded config from {config_path}, PID: {os.getpid()}")
    return _config
