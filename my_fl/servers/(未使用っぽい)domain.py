from fastapi import FastAPI, Depends, WebSocket, APIRouter
from my_fl.core.params import FederateConfig
from my_fl.core.communicators import WebsocketCommunicator
from my_fl.core.manager import ClientDrivenServerManager, IManager
from my_fl.core.store import IStore
from typing import Type


class DB:
    def __init__(self):
        self.db = {"devices": {}, "jobs": {}}

    def register_device(self, mac_address: str):
        self.db["devices"][mac_address] = {"mac": mac_address}

    def create_job(self, config: FederateConfig):
        job_id = 1
        obj = {"id": job_id, "conf": config}
        self.db["jobs"][job_id] = obj
        return obj

    def join_to_job(self, job_id: int, mac_address: str):
        self.db["jobs"][job_id].append(mac_address)


db = DB()


def get_db():
    global db
    yield db


class AppBuilder:
    get_db = None


def build_server(
    *,
    root_prefix: str = "",
    router_prefix: str = "",
    config_store,
    data_store,
    model_store
):
    router = build_websocket_router(
        router_prefix,
        config_store=config_store,
        data_store=data_store,
        model_store=model_store,
    )
    app = FastAPI()
    app.include_router(router, prefix=root_prefix)
    return app


def build_websocket_server(
    manager_cls=ClientDrivenServerManager, *, config_store, data_store, model_store
):
    async def run(websocket):
        comm = WebsocketCommunicator(websocket)
        server = manager_cls(comm, config_store, data_store, model_store)
        async with server as server:
            server.run()

    return run


def build_websocket_router(
    prefix: str = "", path: str = "/federate", *, config_store, data_store, model_store
):
    global get_db

    router = APIRouter(prefix=prefix)

    # @router.on_event("startup")
    # async def startup_event():
    #     ...

    # @router.on_event("shutdown")
    # def shutdown_event():
    #     ...

    # @router.get("/")
    # def index():
    #     return "backend service for Fed_mobile"

    # @router.post("/register_device")
    # def register_device(db: DB = Depends(get_db), *, mac_address: str):
    #     db.register_device(mac_address=mac_address)

    # @router.post("/approve_device")
    # def approve_device(db: DB = Depends(get_db), *, mac_address: str):
    #     ...

    # @router.post("/create_job")
    # def create_job(db: DB = Depends(get_db), *, config: FederateConfig):
    #     return db.create_job(config=config)

    # @router.post("/run_job")
    # def run_job(db: DB = Depends(get_db), *, job_id: int):
    #     ...

    # # websocket
    # @router.websocket("/monitor_job")
    # def monitor_job():
    #     ...
    import logging

    @router.websocket(path)
    async def federate(websocket: WebSocket):
        websocket_server_factory = build_websocket_server(
            WebsocketCommunicator,
            config_store=config_store,
            data_store=data_store,
            model_store=model_store,
        )

        server = websocket_server_factory(websocket)
        await server.run()

        # comm = WebsocketCommunicator(websocket)

        # class ConfigStore(IStore):
        #     async def pull(self, **kwargs):
        #         ...

        # class DataStore(IStore):
        #     async def pull(self, **kwargs):
        #         ...

        # class ModelStore(IStore):
        #     async def pull(self, **kwargs):
        #         ...

        #     async def push(self, **kwargs):
        #         ...

        # server = ClientDrivenServerManager(comm, config_store, data_store, model_store)
        # async with server as server:
        #     server.run()
        # federator = Federator(comm, mode="server")

        # async with federator:
        #     await federator.run()

    class ModelStore:
        ...

    class LocalModelStore:
        ...

    class DbModelStore:
        ...

    class ClientDrivenTrainer:
        def __init__(self, server: IManager, client: IManager):
            self.server = server
            self.client = client

        async def run(self):
            import asyncio

            asyncio.gather(self.serve(), self.execute())

        async def serve(self):
            async with self.server as server:
                await server.run()

        async def execute(self):
            async with self.client as client:
                await client.run()

    return router
