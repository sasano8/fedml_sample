from fastapi import FastAPI, Depends, WebSocket
from my_fl.core.params import FederateConfig
from my_fl.core.communicators import WebsocketServerCommunicator
from my_fl.core.federators import ServerFederator
from typing import Type

app = FastAPI()


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


def build_app(builder: Type[AppBuilder]):
    global get_db

    if builder.get_db is not None:
        get_db = builder.get_db


@app.on_event("startup")
async def startup_event():
    ...


@app.on_event("shutdown")
def shutdown_event():
    ...


@app.get("/")
def index():
    return "backend service for Fed_mobile"


@app.post("/register_device")
def register_device(db: DB = Depends(get_db), *, mac_address: str):
    db.register_device(mac_address=mac_address)


@app.post("/approve_device")
def approve_device(db: DB = Depends(get_db), *, mac_address: str):
    ...


@app.post("/create_job")
def create_job(db: DB = Depends(get_db), *, config: FederateConfig):
    return db.create_job(config=config)


@app.post("/run_job")
def run_job(db: DB = Depends(get_db), *, job_id: int):
    ...


# websocket
@app.websocket("/monitor_job")
def monitor_job():
    ...


@app.websocket("/start_job_1_to_1")
async def start_job_1_to_1(websocket: WebSocket):
    comm = WebsocketServerCommunicator(websocket)
    federator = ServerFederator(comm)

    async with federator:
        await federator.run()


class ModelStore:
    ...


class LocalModelStore:
    ...


class DbModelStore:
    ...


class Trainer:
    def __init__(self, dataloader, model_store):
        if not isinstance(model_store, ModelStore):
            raise Exception()

        self.dataloader = dataloader
        self.model_store = model_store


class Executor:
    def __init__(self, trainer):
        self.trainer = trainer

    def run(self):
        self.dataloader()
        model = self.model_store.load()
        self.executor()
