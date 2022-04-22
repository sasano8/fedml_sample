import typer

common_opt = {"no_args_is_help": True}

app = typer.Typer(**common_opt)
config = typer.Typer(**common_opt)
server = typer.Typer(**common_opt)
model = typer.Typer(**common_opt)
loader = typer.Typer(**common_opt)
train = typer.Typer(**common_opt)
federate = typer.Typer(**common_opt)

class LoadConfigError(Exception):
    ...

class ConfigKeyError(Exception):
    ...

class InvalidConfigError(Exception):
    ...


def load_config(config_name: str = None):
    if config_name is None:
        config_name = "default"

    default_config = {"default": {}}
    override = {}
    config = dict(**default_config, **override)
    
    try:
        return config[config_name]
    except KeyError:
        raise ConfigKeyError(config_name)


@app.command()
def init(config_name: str = "default", ignore_if_exists: bool = False):
    ...

@app.command()
def login(token: str = None):
    ...

@app.command()
def logout():
    ...

@app.command()
def purge():
    ...

@config.command()
def list(config_name: str = None):
    ...

@config.command()
def validate(config_name: str = None):
    ...

@config.command()
def show(config_name: str = None):
    config = load_config(config_name)

@config.command()
def pull(config_name: str = None):
    config = load_config(config_name)

@config.command()
def set(config_name: str = None):
    config = load_config(config_name)

@loader.command()
def list(config_name: str = None):
    config = load_config(config_name)

@loader.command()
def run(config_name: str = None):
    config = load_config(config_name)

@loader.command()
def dry_run(config_name: str = None):
    config = load_config(config_name)

@loader.command()
def show(config_name: str = None, n: int = None):
    config = load_config(config_name)

@train.command()
def list(config_name: str = None):
    config = load_config(config_name)

@train.command()
def run(config_name: str = None, standalone: bool = False):
    config = load_config(config_name)

@train.command()
def dry_run(config_name: str = None, standalone: bool = False):
    config = load_config(config_name)

@federate.command()
def list(config_name: str = None):
    config = load_config(config_name)

@federate.command()
def join(config_name: str = None):
    config = load_config(config_name)

@federate.command()
def run(config_name: str = None):
    config = load_config(config_name)

@federate.command()
def dry_run(config_name: str = None):
    config = load_config(config_name)

@server.command()
def list(config_name: str = None):
    config = load_config(config_name)

@server.command()
def start(config_name: str = None):
    config = load_config(config_name)

@server.command()
def stop(config_name: str = None):
    config = load_config(config_name)

@model.command()
def list(config_name: str = None):
    config = load_config(config_name)

@model.command()
def pull(config_name: str = None):
    config = load_config(config_name)

@model.command()
def push(config_name: str = None):
    config = load_config(config_name)

app.add_typer(config, name="config")
app.add_typer(server, name="server")
app.add_typer(model, name="model")
app.add_typer(loader, name="loader")
app.add_typer(train, name="train")
app.add_typer(federate, name="federate")
