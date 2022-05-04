import pytest
from my_fl.core.workspace import WorkSpace
from my_fl.server_factories import build_server
from functools import wraps
import asyncio


def to_sync(async_func):
    @wraps(async_func)
    def wrapper(*args, **kwargs):
        coro = async_func(*args, **kwargs)
        return asyncio.run(coro)

    return wrapper


def create_server(config=None):
    with WorkSpace.as_tmp_dir() as dir:
        dir.init()
        # dir.set_config(config)
        config_store, data_store, model_store = dir.get_stores()

        server = build_server(
            config_store=config_store, data_store=data_store, model_store=model_store
        )
        yield server


@pytest.fixture(scope="function")
def local_server():
    yield from create_server(config={})


@pytest.fixture(scope="function")
def remote_server():
    yield from create_server(config={})


@to_sync
async def test_standalone_cross_device():
    import time
    from my_fl import execute_server, WorkSpace

    with WorkSpace.as_tmp_dir() as ws:
        with execute_server(ws.path):
            print(1)
            print(2)
            print(3)
            time.sleep(10)


def test_standalone_cross_silo():
    ...
