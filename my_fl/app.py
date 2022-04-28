from fastapi import FastAPI, Depends, WebSocket
from .params import FederateConfig


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
    comm = WebsocketCommunicator(websocket)
    manager = ManagerForWebsocket(comm, mode="server")

    async with manager:
        await manager.run()


class CommunicatorBase:
    async def __aenter__(self):
        await self.accept()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def accept(self):
        raise NotImplementedError()

    async def close(self):
        raise NotImplementedError()

    async def send_bytes(self, data):
        raise NotImplementedError()

    async def send_json(self, data):
        raise NotImplementedError()

    async def receive_bytes(self):
        raise NotImplementedError()

    async def receive_json(self):
        raise NotImplementedError()

    async def send_msg(self, msg: str, data=None):
        if isinstance(data, bytes):
            obj = {"type": "bytes", "msg": msg}
            await self.send_json(obj)
            await self.send_bytes(data)
        else:
            obj = {"type": "json", "msg": msg, "data": data}
            await self.send_json(obj)

    async def wait_msg(self, msg: str):
        data = await self.receive_json()
        if data["msg"] != msg:
            raise Exception("msg mismatch.")

        if data["type"] == "json":
            return data["data"]
        elif data["type"] == "bytes":
            return await self.receive_bytes()
        else:
            raise Exception(f"Unkown msg type: {data['type']}")


class WebsocketCommunicator(CommunicatorBase):
    def __init__(self, websocket: WebSocket):
        self.comm = websocket

    async def accept(self) -> None:
        await self.comm.accept()

    async def close(self):
        await self.comm.close()

    async def send_bytes(self, data) -> None:
        await self.comm.send_bytes(data)

    async def send_json(self, data) -> None:
        await self.comm.send_json(data)

    async def receive_bytes(self):
        return await self.comm.receive_bytes()

    async def receive_json(self):
        return await self.comm.receive_json()


class ManagerForWebsocket:
    def __init__(self, websocket: CommunicatorBase, mode: str = "server"):
        self.websocket = websocket
        self.mode = mode

    async def __aenter__(self):
        await self.websocket.accept()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.websocket.close()

    def is_server(self):
        return self.mode == "server"

    def is_client(self):
        return self.mode == "client"

    async def run(self):
        if self.mode == "client":
            await self.s1_send_identifer()
            await self.s3_recieve_job_config_and_send_ok()
            await self.s5_revieve_model_and_send_model_diff()  # train on client
            await self.s7_revieve_model_and_send_ok()
        elif self.mode == "server":
            await self.s2_recieve_identifier_and_send_job_config()
            await self.s4_recieve_ok_and_send_model()  # train on server
            await self.s6_revieve_model_diff_and_send_model()  # aggregate/transfer
            await self.s8_revieve_ok()
        else:
            raise Exception()

    async def s1_send_identifer(self):
        await self.websocket.send_msg(
            "s1_send_identifer", "mac_address"
        )  # device or server host?
        # await self.websocket.send_json({"msg": "mac_address"})  # device or server host?

    async def s2_recieve_identifier_and_send_job_config(self):
        identifier = await self.websocket.wait_msg("s1_send_identifer")
        msg = {"msg": "job_config"}
        await self.websocket.send_json(msg)

    async def s3_recieve_job_config_and_send_ok(self):
        result = await self.websocket.receive_json()
        msg = {"msg": "ok"}
        await self.websocket.send_json(msg)

    async def s4_recieve_ok_and_send_model(self):
        result = await self.websocket.receive_json()
        msg = {"msg": "send_binary_model"}
        await self.websocket.send_json(msg)

    async def s5_revieve_model_and_send_model_diff(self):
        msg = await self.websocket.receive_json()
        await self.websocket.send_json({"msg": "global_parameter"})

    async def s6_revieve_model_diff_and_send_model(self):
        msg = await self.websocket.receive_json()
        await self.websocket.send_json({"msg": "aggrated_model"})

    async def s7_revieve_model_and_send_ok(self):
        msg = await self.websocket.receive_json()
        await self.websocket.send_json({"msg": "ok"})

    async def s8_revieve_ok(self):
        msg = await self.websocket.receive_json()


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
