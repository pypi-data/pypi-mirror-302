from fastapi import FastAPI, Response
from pydantic import BaseModel
from loguru import logger
import pickle
import pathlib
import requests
from vmc.utils.utils import get_freer_gpu, find_available_port


def check_server_status(port: int):
    try:
        ret = requests.get(f"http://localhost:{port}/ping")
    except Exception as e:
        logger.error(f"Failed to check if manager is started: {e}")
        return False
    if ret.status_code == 200:
        return True
    return False


def save_model(model, path: str = ".manager/started_models.pkl"):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)


def load_model(path: str = ".manager/started_models.pkl"):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not pathlib.Path(path).exists():
        return {}
    with open(path, "rb") as f:
        models = pickle.load(f)
        alive_models = {}
        for model, port in models.items():
            if check_server_status(port):
                alive_models[model] = port
            else:
                logger.warning(f"model server {model} is dead")
    save_model(alive_models)
    logger.info(f"loaded models: {alive_models}")
    return alive_models


# catch ctrl+c
def signal_handler(sig, frame):
    import os

    logger.info("Received SIGINT, stopping all servers")
    for port in started_models.values():
        os.system(f"kill -9 $(lsof -t -i:{port})")
    exit(0)


app = FastAPI()
started_models = load_model()


class BaseResponse(BaseModel):
    code: int = 200
    msg: str = "success"

    def r(self):
        return Response(status_code=self.code, content=self.model_dump_json())


class StartServerResponse(BaseResponse):
    port: int = 0


class StartServerParams(BaseModel):
    id: str
    config_path: str
    max_gpu_usage: int = 1
    exclude_gpus: list[int] = []


class StopServerParams(BaseModel):
    id: str | None = None


@app.post("/start-server")
async def start_server(params: StartServerParams):
    import os

    if params.id in started_models and check_server_status(started_models[params.id]):
        return StartServerResponse(port=started_models[params.id]).r()

    devices = ",".join(
        [
            str(x)
            for x in get_freer_gpu(
                params.max_gpu_usage,
                params.exclude_gpus,
            )
        ]
    )
    port = find_available_port()
    cmd = [
        f"CUDA_VISIBLE_DEVICES={devices}",
        "ms",
        "start",
        "--config-path",
        params.config_path,
        "--model-id",
        params.id,
        "--port",
        str(port),
        "-d",
    ]
    cmd = " ".join(cmd)
    logger.info(f"start model server: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        return BaseResponse(code=500, msg=f"failed to start model server: {ret}").r()

    started_models[params.id] = port
    save_model(started_models)
    return StartServerResponse(port=port).r()


@app.post("/stop-server")
async def stop_server(params: StopServerParams):
    import os

    if params.id not in started_models:
        return BaseResponse(code=404, msg="model server not found").r()
    stop_ports = (
        list(started_models.values())
        if params.id is None
        else [started_models[params.id]]
    )
    logger.info(f"stop model server: {stop_ports}")
    for port in stop_ports:
        ret = os.system(f"kill -9 $(lsof -t -i:{port})")
        if ret != 0:
            logger.warning(f"failed to stop model server: {params.id}")
    if params.id is None:
        started_models.clear()
    else:
        started_models.pop(params.id)
    save_model(started_models)
    return BaseResponse().r()


@app.get("/list-servers")
async def list_servers():
    return started_models


@app.get("/ping")
async def ping():
    return BaseResponse().r()
