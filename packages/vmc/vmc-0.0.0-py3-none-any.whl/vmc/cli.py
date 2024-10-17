import click


@click.group()
@click.version_option()
def cli():
    pass


@cli.group()
def manager():
    pass


@cli.group()
def dashboard():
    pass


def get_last_commit_message():
    import subprocess

    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"], universal_newlines=True
        ).strip()
    except subprocess.CalledProcessError:
        return "Unknown"


def get_version():
    import importlib.metadata

    return importlib.metadata.version("vmc")


@dashboard.command(name="start")
@click.option("--config-path", default=None)
@click.option("--detach", "-d", is_flag=True)
def start_dashboard(config_path: str, detach: bool):
    import os
    from vmc.config import get_config

    port = get_config(config_path).dashboard.port
    os.system(
        f"gunicorn -b 127.0.0.1:{port} "
        f"-k uvicorn.workers.UvicornWorker "
        f"-e CONFIG_PATH={config_path} "
        f"vmc.dashboard:demo {'-D' if detach else ''}"
    )


@dashboard.command(name="stop")
@click.option("--config-path", default=None)
@click.option("--port", "-p", default=None)
def stop_dashboard(config_path: str | None, port: int | None = None):
    import os
    from vmc.config import get_config

    dashboard_port = get_config(config_path).dashboard.port
    if port:
        dashboard_port = port

    ret = os.system(f"kill -9 $(lsof -t -i:{dashboard_port})")
    if ret != 0:
        print("Dashboard not running")
    else:
        print("Dashboard stopped")


@dashboard.command(name="reload")
@click.option("--config-path", default=None)
def reload_dashboard(config_path: str):
    import os
    from vmc.config import get_config

    config = get_config(config_path).dashboard

    ret = os.system(
        f"kill -HUP $(lsof -t -i:{config.port}) && echo 'Dashboard reloaded'"
    )
    if ret != 0:
        print("Dashboard not running")


@cli.command(name="start")
@click.option("--config-path", default=None)
@click.option("--detach", "-d", is_flag=True)
@click.option("--model-id", "-m", default=None)
@click.option("--port", "-p", default=None)
def start_server(
    config_path: str, detach, model_id: str | None = None, port: int | None = None
):
    import os
    import anyio
    from vmc.config import get_config
    from vmc.utils.lark import get_lark_client

    config = get_config(config_path)
    workers = config.app.workers

    env = {"CONFIG_PATH": config.config_path}
    if model_id:
        workers = 1
        env["LOG_REQUESTS"] = "false"
        env["CHECK_AUTH"] = "false"
        env["MODEL_ID"] = model_id
    env = " ".join([f"-e {k}={v}" for k, v in env.items()])

    if config.app.init_user and not model_id:
        from vmc.utils.auth import create_user

        create_user(config.app.init_user, config.app.init_pass)

    if model_id:
        title = f"{model_id} server started"
        msg = f"Port {port or config.app.port}\nModel ID: {model_id}"
    else:
        title = f"Modelhub {get_version()} started"
        msg = get_last_commit_message()
    anyio.run(get_lark_client().webhook.post_success_card, msg, title)
    os.system(
        f"gunicorn -w {workers} -b {config.app.host}:{port or config.app.port} "
        f"--worker-class uvicorn.workers.UvicornWorker "
        f"--timeout 300 "
        f"{env} "
        "--log-level info "
        f"vmc.server:app {'-D' if detach else ''}"
    )


@manager.command(name="start")
@click.option("--config-path", default=None)
@click.option("--detach", "-d", is_flag=True)
def start_manager(config_path: str, detach: bool):
    from vmc.config import get_config
    import os

    config = get_config(config_path).app

    os.system(
        f"gunicorn -b {config.host}:{config.manager_port} "
        f"-k uvicorn.workers.UvicornWorker "
        f"vmc.manager.app:app {'-D' if detach else ''}"
    )


@manager.command(name="stop")
@click.option("--config-path", default=None)
@click.option("--port", "-p", default=None)
def stop_manager(config_path: str | None, port: int | None = None):
    import os
    from vmc.config import get_config

    if config_path:
        manager_port = get_config(config_path).app.manager_port
    if port:
        manager_port = port

    ret = os.system(f"kill -9 $(lsof -t -i:{manager_port})")
    if ret != 0:
        print("Manager not running")
    else:
        print("Manager stopped")


@manager.command(name="reload")
@click.option("--config-path", default=None)
def reload_manager(config_path: str):
    import os
    from vmc.config import get_config

    config = get_config(config_path).app

    ret = os.system(
        f"kill -HUP $(lsof -t -i:{config.manager_port}) && echo 'Manager reloaded'"
    )
    if ret != 0:
        print("Manager not running")


if __name__ == "__main__":
    cli()
