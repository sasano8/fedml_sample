from my_fl.core.communicators import StandaloneCommunicator
from my_fl.core.federators import ServerFederator, ClientFederatorBase


class ClientBase:
    def login(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()


class StandaloneClient(ClientBase):
    def __init__(self, cwd):
        self.comm = StandaloneCommunicator()

    async def run(self):
        server = ServerFederator(self.comm)

        async with server:
            import asyncio

            asyncio.gather(server.run(), self._run_client())

    async def _run_client(self):
        comm = self.comm
        await comm.send("s1_send_identifer", "mac_address")
        await comm.wait("s2_recieve_identifier_and_send_job_config")
        await comm.wait("s4_recieve_ok_and_send_model")
        await comm.wait("s6_revieve_model_diff_and_send_model")
        await comm.send("s7_revieve_model_and_send_ok")

    async def on_connect(self, val):
        ...


class RemoteClient(ClientBase):
    def __init__(self, host):
        ...
