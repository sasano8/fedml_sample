from fastapi import WebSocket


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

    async def send(self, msg: str, data=None):
        if isinstance(data, bytes):
            obj = {"type": "bytes", "msg": msg}
            await self.send_json(obj)
            await self.send_bytes(data)
        else:
            obj = {"type": "json", "msg": msg, "data": data}
            await self.send_json(obj)

    async def wait(self, msg: str):
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
