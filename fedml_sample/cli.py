import os
import json
import typer


common_opt = {"no_args_is_help": True}

app = typer.Typer(**common_opt)
config = typer.Typer(**common_opt)
server = typer.Typer(**common_opt)
model = typer.Typer(**common_opt)
loader = typer.Typer(**common_opt)
train = typer.Typer(**common_opt)
federate = typer.Typer(**common_opt)


default_conf = {
    "version": "0.1",
    "federation": [
        "fedavg",
        {
            "config_name": "config_1",
            "description": "",
            "output_model_name": "mymodel",
            "allow_anonymous_domain": True,
            "allow_anonymous_device": True,
        },
    ],
    "topology": ["vertical", {"upstream": "xxx.com"}],  # or p2p
    "manager": ["client"],
    # "manager": [
    #     "server",
    #     {
    #         "comm_round": 1,
    #         "batch_size": 1,
    #         "epochs": 1,
    #         "client_optimizer": "",
    #         "lr": 1,
    #         "ci": 0,
    #         "partition_method": "hetero",
    #         "client_num_in_total": 1,
    #         "client_num_per_round": 1
    #     }
    # ],
    "distributed": [
        "distributed",  # standalone, distributed, auto
        {"gpu": 0, "communicator": "mpi", "nodes": []},  # or grpc hosts
    ],
    "trainer": ["MyModelTrainerTAG", {}],
    "loader": [
        "fileloader",
        {"type": "csv", "path": "aaa/bbb/ccc/aaaa.csv", "cache": True},
    ],
    "model": ["LogisticRegression", {"input_dim": 1, "output_dim": 1}],
}


class LoadConfigError(Exception):
    ...


class ConfigKeyError(Exception):
    ...


class InvalidConfigError(Exception):
    ...


# TODO: 第一階層しか対応していない
def deep_merge(dic1, dic2):
    result = {}
    for k, v in dic1.items():
        if k in dic2:
            v = dict(v, **dic2[k])
        else:
            ...

        result[k] = v

    return result


class Config:
    def __init__(self, path):
        if isinstance(path, str):
            from pathlib import Path

            path = Path(path)

        conf_dir = path / ".fed"
        self.dir_root = conf_dir
        self.cache = conf_dir / "cache"
        self.file_conf = conf_dir / "conf.json"
        self.file_override = conf_dir / "conf.override.json"
        self.file_ignore = conf_dir / ".gitignore"

    @classmethod
    def from_cwd(cls):
        conf = cls(os.getcwd())
        return conf

    def init(self):
        dir_root = self.dir_root
        dir_cache = self.cache
        file_conf = self.file_conf
        file_override = self.file_override
        file_ignore = self.file_ignore

        if not dir_root.exists():
            os.mkdir(dir_root)

        if not dir_cache.exists():
            os.mkdir(dir_cache)

        if not file_conf.exists():
            with open(file_conf, "w") as f:
                json.dump({"default": default_conf}, f, indent=2, ensure_ascii=False)

        if not file_override.exists():
            with open(file_override, "w") as f:
                json.dump({"default": {}}, f, indent=2, ensure_ascii=False)

        if not file_ignore.exists():
            with open(file_ignore, "w") as f:
                f.write("""cache""")

    def load(self):
        with open(self.file_conf) as f:
            conf = json.load(f)

        with open(self.file_override) as f:
            override = json.load(f)
            conf = deep_merge(conf, override)

        return conf

    def get(self, config_name: str = None):
        conf = self.load()

        if config_name is None:
            config_name = "default"

        try:
            return conf[config_name]
        except KeyError:
            raise ConfigKeyError(config_name)


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


@server.command()
def list(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def start(config_name: str = None):
    conf = Config.from_cwd().get(config_name)


@server.command()
def stop(config_name: str = None):
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


app.add_typer(config, name="config")
app.add_typer(server, name="server")
app.add_typer(model, name="model")
app.add_typer(loader, name="loader")
app.add_typer(train, name="train")
app.add_typer(federate, name="federate")
