import time
from typing import List

from loguru import logger
from pydantic.v1 import BaseModel, Field

import vmc.models.api as api_module
import vmc.models.local as local_module
from vmc.types.errors.errors import ModelNotFoundError

from vmc.config import ModelConfig, get_config, ProviderConfig
from vmc.models._base import BaseChatModel, BaseCrossEncoderModel
from vmc.models.local.whisper import BaseAudioModel
from vmc.models.api.modelhub import ModelhubModel
from vmc.manager.interface import start_local_server


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


def uniform(id: str):
    return id.lower().replace("-", "").strip()


def validate_models(providers: list[ProviderConfig]):
    models: dict[str, ModelConfig] = {}
    credentials: dict[str, list[dict]] = {}
    for p in providers:
        for m in p.models:
            id_ = uniform(m.name)
            if id_ in models:
                msg = f"model {id_} already exists, using {p.provider_name}/{m.name}"
                id_ = f"{p.provider_name}/{m.name}"
                logger.warning(msg)
            if m.is_local and not hasattr(local_module, m.class_name):
                raise ValueError(f"model {m.name} not found in local models")
            if not m.is_local and not hasattr(api_module, m.class_name):
                raise ValueError(f"model {m.name} not found in api models")
            models[id_] = m
            credentials[id_] = p.credentials
    return models, credentials


def unload_model_from_gpu():
    import torch

    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()


class ModelFactory(object):
    def __init__(self, providers: list[ProviderConfig]) -> None:
        """提供各种模型，包括embedding的模型和llm的模型"""
        self._model_list, self._credentials = validate_models(providers)
        self._cache = {}
        self.init_id = get_config().app.init_model_id
        if self.init_id:
            logger.info(f"Initializing model {self.init_id}")
            model = self._model_list[uniform(self.init_id)]
            self._cache[uniform(self.init_id)] = getattr(
                local_module, model.class_name
            )(**model.init_kwargs, config=model)

    @property
    def models(self):
        return {m.name: m.dump() for m in self._model_list.values()}

    async def aget(
        self, id: str
    ) -> BaseChatModel | BaseAudioModel | BaseCrossEncoderModel:
        id = uniform(id)
        if id in self._cache:
            model = self._model_list[id]
            if isinstance(self._cache[id], ModelhubModel):
                if not self._cache[id].alive():
                    logger.warning(f"model {id} is not alive, reloading")
                    del self._cache[id]
                else:
                    return self._cache[id]
            else:
                return self._cache[id]
        if id not in self._model_list:
            msg = f"model {id} not found"
            logger.error(msg)
            raise ModelNotFoundError(msg=msg)

        model = self._model_list[id]
        credentials = self._credentials[id]

        if not model.is_local:
            kwargs = {**model.init_kwargs, "config": model}
            if "credentials" not in kwargs:
                kwargs["credentials"] = credentials
            self._cache[id] = getattr(api_module, model.class_name)(**kwargs)
        else:
            logger.info(f"starting local server for {model.name}")
            port = start_local_server(
                model.name,
                get_config().config_path,
                max_gpu_usage=model.max_gpu_usage,
                exclude_gpus=get_config().app.exclude_gpus,
            )
            self._cache[id] = ModelhubModel(
                host=f"http://{get_config().app.manager_host}:{port}",
                model_id=model.name,
                config=model,
            )
        return self._cache[id]


_model_factory = None


def get_model_factory():
    global _model_factory
    if _model_factory is None:
        _model_factory = ModelFactory(get_config().providers)
    return _model_factory
