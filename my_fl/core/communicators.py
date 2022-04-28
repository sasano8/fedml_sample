import json
from typing import TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from fastapi import WebSocket
else:
    WebSocket = None


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


class WebsocketServerCommunicator(CommunicatorBase):
    def __init__(self, websocket: WebSocket):
        if not isinstance(websocket, WebSocket):
            raise Exception()

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


class WebsocketClientCommunicator(CommunicatorBase):
    ...


class StandaloneCommunicator(CommunicatorBase):
    def __init__(self, buf):
        from collections import deque

        self.buf = deque()

    async def accept(self) -> None:
        ...

    async def close(self) -> None:
        ...

    async def send_bytes(self, data) -> None:
        if not isinstance(data, bytes):
            raise TypeError()
        self.buf.append(data)

    async def send_json(self, data) -> None:
        self.buf.append(json.dumps(data))

    async def receive_bytes(self):
        buff = self.buff
        while not buff:
            await asyncio.sleep(0.05)

        data = self.buf.popleft()

        if isinstance(data, str):
            return data.encode("utf-8")
        elif isinstance(data, bytes):
            return data
        else:
            raise TypeError()

    async def receive_json(self):
        buff = self.buff
        while not buff:
            await asyncio.sleep(0.05)

        data = self.buf.popleft()
        return json.load(data)
