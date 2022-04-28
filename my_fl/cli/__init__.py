import json
import typer

from my_fl.core.directory import RootDir as Config, LocalRepository

common_opt = {"no_args_is_help": True}

app = typer.Typer(**common_opt)
config = typer.Typer(**common_opt)
server = typer.Typer(**common_opt)
domain = typer.Typer(**common_opt)
dataset = typer.Typer(**common_opt)
model = typer.Typer(**common_opt)
loader = typer.Typer(**common_opt)
train = typer.Typer(**common_opt)
federate = typer.Typer(**common_opt)


@app.command()
def init():
    Config.from_cwd().init()


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
    conf = Config.from_cwd().get(config_name)


@config.command()
def show(config_name: str = None):
    conf = Config.from_cwd().get(config_name)
    typer.echo(json.dumps(conf, indent=2, ensure_ascii=False))


@config.command()
def pull(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@config.command()
def set(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@loader.command()
def list(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@loader.command()
def run(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@loader.command()
def dry_run(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@loader.command()
def show(config_name: str = None, n: int = None):
    conf = Config.from_cwd().get(config_name)


@train.command()
def list(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@train.command()
def run(config_name: str = None, standalone: bool = False):
    conf = Config.from_cwd().get(config_name)


@train.command()
def dry_run(config_name: str = None, standalone: bool = False):
    conf = Config.from_cwd().get(config_name)


@federate.command()
def list(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@federate.command()
def join(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@federate.command()
def run(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@federate.command()
def dry_run(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@dataset.command("list")
def dataset_list(config_name: str = None):
    dir = Config.from_cwd()
    conf = dir.get(config_name)
    typer.echo(LocalRepository(dir).get_datasets())


@dataset.command("show")
def dataset_show(name: str, *, config_name: str = None):
    dir = Config.from_cwd()
    conf = dir.get(config_name)
    typer.echo(LocalRepository(dir).get_dataset(name))


@dataset.command("pull")
def dataset_pull(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@dataset.command("push")
def dataset_push(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@model.command()
def list(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@model.command()
def pull(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@model.command()
def push(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def hosts(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def devices(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def users(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def start(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def stop(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@domain.command()
def hosts(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@domain.command()
def devices(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@domain.command()
def users(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@domain.command()
def start(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@domain.command()
def stop(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


app.add_typer(config, name="config")
app.add_typer(server, name="server")
app.add_typer(domain, name="domain")
app.add_typer(dataset, name="dataset")
app.add_typer(model, name="model")
app.add_typer(loader, name="loader")
app.add_typer(train, name="train")
app.add_typer(federate, name="federate")
