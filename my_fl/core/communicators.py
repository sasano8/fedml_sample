import json
from typing import TYPE_CHECKING, Tuple, Any, TypedDict, Union
import asyncio

if TYPE_CHECKING:
    from fastapi import WebSocket
    from starlette.websockets import WebSocketState
else:
    WebSocket = None


class ResultMsg(TypedDict):
    is_error: bool
    info: dict


class CommunicatorBase:
    def __init__(self):
        self.events: list = None

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

    def is_closed(self):
        raise NotImplementedError()

    async def wait_disconnected(self, interval: float = 0.1):
        while not self.is_closed():
            await asyncio.sleep(interval)

    async def send(self, msg: str, data=None, info: Any = None):
        if isinstance(data, bytes):
            obj = {"type": "bytes", "msg": msg, "info": info}
            await self.send_json(obj)
            await self.send_bytes(data)
        else:
            obj = {"type": "json", "msg": msg, "info": info, "data": data}
            await self.send_json(obj)

    async def wait(self, msg: str) -> Tuple[ResultMsg, Any]:
        data = await self.receive_json()
        if data["msg"] != msg:
            raise Exception("msg mismatch.")

        if data["type"] == "json":
            return data["info"], data["data"]
        elif data["type"] == "bytes":
            return data["info"], await self.receive_bytes()
        else:
            raise Exception(f"Unkown msg type: {data['type']}")

    async def request(self, msg: str, data=None, info: dict = None):
        await self.send(msg, data, info)
        return await self.wait(msg)

    def add_events(self, events: Union[list, dict]):
        if self.events is not None:
            raise RuntimeError()

        if isinstance(events, list):
            events = {x.__name__: x for x in events}

        if not isinstance(events, dict):
            raise TypeError()

        if not hasattr(self, "events"):
            self.events = events.copy()
        else:
            self.events = {**self.events, **events}


class WebsocketCommunicator(CommunicatorBase):
    def __init__(self, websocket: WebSocket):
        if not isinstance(websocket, WebSocket):
            raise Exception()

        self.comm = websocket

    async def accept(self) -> None:
        await self.comm.accept()

    async def close(self):
        await self.comm.close()

    def is_closed(self):
        return self.comm.application_state == WebSocketState.DISCONNECTED

    async def send_bytes(self, data) -> None:
        await self.comm.send_bytes(data)

    async def send_json(self, data) -> None:
        await self.comm.send_json(data)

    async def receive_bytes(self):
        return await self.comm.receive_bytes()

    async def receive_json(self):
        return await self.comm.receive_json()


class StandaloneCommunicator(CommunicatorBase):
    def __init__(self):
        from collections import deque

        self.buf = deque()
        self._is_closed = False

    async def accept(self) -> None:
        ...

    async def close(self) -> None:
        ...

    def is_closed(self):
        return self._is_closed

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


class MultiprocessCommunicator(StandaloneCommunicator):
    def __init__(self):
        raise NotImplementedError()


class DistrebutedCommunicator(StandaloneCommunicator):
    def __init__(self):
        raise NotImplementedError()
