class ClientBase:
    def login(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()


class LocalClient(ClientBase):
    def __init__(self, cwd):
        ...


class RemoteClient(ClientBase):
    def __init__(self, host):
        ...
