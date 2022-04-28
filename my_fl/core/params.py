from pydantic import BaseModel
from typing import Tuple, Union

# class Discriminator(NamedTuple):
#     name: str
#     args: dict = {}

Discriminator = Tuple[str, Union[dict, None]]


class FederateConfig(BaseModel):
    version: str
    federation: Discriminator
    manager: Discriminator
    distributed: Discriminator = ("standalone", None)
    trainer: Discriminator
    loader: Discriminator
    model: Discriminator

    class Config:
        schema_extra = {
            "examples": [
                {
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
            ]
        }
