import os
import json

from .exceptions import ConfigKeyError


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


class RootDir:
    def __init__(self, path):
        if isinstance(path, str):
            from pathlib import Path

            path = Path(path)

        conf_dir = path / ".fed"

        self.cache = conf_dir / "cache"
        self.datasets = conf_dir / "datasets"
        self.models = conf_dir / "models"
        self.file_conf = conf_dir / "conf.json"
        self.file_override = conf_dir / "conf.override.json"
        self.file_ignore = conf_dir / ".gitignore"

        self.dir_root = conf_dir

    @classmethod
    def from_cwd(cls):
        conf = cls(os.getcwd())
        return conf

    def init(self):
        dir_root = self.dir_root
        dir_cache = self.cache
        dir_datasets = self.datasets
        dir_models = self.models
        file_conf = self.file_conf
        file_override = self.file_override
        file_ignore = self.file_ignore

        if not dir_root.exists():
            os.mkdir(dir_root)

        if not dir_cache.exists():
            os.mkdir(dir_cache)

        if not dir_datasets.exists():
            os.mkdir(dir_datasets)

        if not dir_models.exists():
            os.mkdir(dir_models)

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


class LocalRepository:
    def __init__(self, conf: RootDir):
        self.conf = conf

    def get_datasets(self):
        return [x.name for x in self.conf.datasets.iterdir()]

    def get_dataset(self, name: str):
        with open(self.conf.datasets / name) as f:
            return f.read()

    def get_models(self):
        return [x.name for x in self.conf.models.iterdir() if x.is_file()]
