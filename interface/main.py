from fastapi import FastAPI, Query, Request
from pydantic import BaseModel, Field
from typing import Literal, List

app = FastAPI()

# "--gpu=0",
#         "--dataset=fed_shakespeare",
#         "--data_dir=./../../../data/fed_shakespeare/datasets",
#         "--model=rnn",
#         "--partition_method=hetero",
#         "--client_num_in_total=10",
#         "--client_num_per_round=10",
#         "--comm_round=1000",
#         "--epochs=1",
#         "--batch_size=10",
#         "--client_optimizer=sgd",
#         "--lr=0.8",
#         "--ci=0"

MODELS = Literal["rnn", "resnet56", "lr", "cnn", "resnet18_gn", "mobilenet"]
OPTIMIZERS = Literal["sgd", "adam"]
PARTITION_METHODS = Literal["hetero", "homo"]  # heterogeneity 不均一性  homogeneous 同種性
# DISTRIBUTIONS = Literal["homo", "lumo"]  # 満足がいくデータセットが得られない場合に、テストデータセットを予測し、データセットを補完する？

class MpiHost(BaseModel):
    """
    計算を実行する
    """

    host: str = Field(description="host名またはipを指定")
    slots: int = Field(description="CPU数を指定")


@app.post("/create_mpi_host_file")
def create_mpi_host_file(mpi_host_file: List[MpiHost]):
    """
    形式はバージョンにより２つある。
    node1:4
    node1 slots=4
    """
    return "\n".join(x.host + f":{x.slots}" for x in mpi_host_file.__root__)

@app.post("/fedavg")
def fedavg(
    *,
    gpu: int = Query(0, description=""),
    dataset: str,
    data_dir: str,
    model: MODELS = "rnn",
    partition_method: PARTITION_METHODS = Query("hetero", description="how to partition the dataset on local workers"),
    client_num_in_total: int = Query(1, description="number of workers in a distributed cluster"),
    client_num_per_round: int = Query(1, description="number of workers"),
    comm_round: int = Query(2, description="how many round of communications we should use. roundの数だけepochsを繰り返すようだ。"),
    batch_size: int = Query(..., description="データセットを指定したサイズの塊に分割する。大きいほど処理速度が速いが、局所解に陥りやすく、また、メモリ消費量が大きい。"),
    epochs: int = Query(
        1,
        # description="It specifies the number of iterations. Epoch mean one complete pass of the training dataset through the algorithm."
        description="batch_sizeを元のデータセット分反復することを1エポック。通常数エポック実行する。",
    ),
    client_optimizer: OPTIMIZERS,
    lr: float = Query(0.0001, description="学習率"),
    ci: int = Query(0, description="CPUベースで計算します。ただし、トレーニング速度が遅くなるため、クライアントのテストのみ実行されます。")
):
    "${workspaceFolder}/fedml_experiments/standalone/fedavg"


@app.post("/fedavg_internal")
def fedavg_internal(dataset, device, args, model_trainer):
    ...


@app.post("/train")
def train(table_name, output_model_name, params: dict):
    ...


@app.post("/instantiate_model")
def instantiate_model(model_name: str, model_args: dict):
    import torch
    torch.nn.Module
    model_args = {"output_dim": 1}
    LogisticRegression
    CNN_DropOut
    resnet18
    RNN_OriginalFedAvg
    LogisticRegression
    RNN_StackOverFlow
    resnet56
    mobilenet


@app.post("/instantiate_trainer")
def instantiate_trainer(trainer_name: str, trainer_args: dict, model=None):
    """トレーナは、データロード、学習、テスト、グローバルパラメータの更新など、
    一連の学習工程を管理するオブジェクトである。
    """
    MyModelTrainerTAG(model)
    MyModelTrainerNWP(model)
    MyModelTrainerCLS(model)



@app.post("/instantiate_federator")
def instantiate_federator(trainer=None, *, args: dict, client_id: int, backend: str = "MQTT"):
    """フェデレータは複数のトレーナの調整役である。
    """




from typing import NamedTuple, Tuple, Union

# class Discriminator(NamedTuple):
#     name: str
#     args: dict = {}

Discriminator = Tuple[str, Union[dict, None]]

class FederateConfig(BaseModel):
    version: str
    federation: Discriminator
    manager: Discriminator
    distributed: Discriminator = ("standalone",)
    trainer: Discriminator
    loader: Discriminator
    model: Discriminator

    class Config:
        schema_extra = {
            'examples': [
                {
                    "version": "0.1",
                    "federation": [
                        "fedavg",
                        {
                            "config_name": "config_1",
                            "description": "",
                            "output_model_name": "mymodel",
                            "allow_anonymous_domain": True,
                            "allow_anonymous_device": True
                        }
                    ],
                    "topology": [
                        "vertical",  # or p2p
                        {
                            "upstream": "xxx.com"
                        }
                    ],
                    "manager": [
                        "client"
                    ],
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
                        {
                            "gpu": 0,
                            "communicator": "mpi",
                            "nodes": []
                        }
                    ],
                    "trainer": [
                        "MyModelTrainerTAG",
                        {}
                    ],
                    "loader": [
                        "fileloader",
                        {
                            "type": "csv",
                            "path": "aaa/bbb/ccc/aaaa.csv",
                            "cache": True
                        }
                    ],
                    "model": [
                        "LogisticRegression",
                        {
                            "input_dim": 1,
                            "output_dim": 1
                        }
                    ]
                }
            ]
        }


class FederateFactory:
    def __init__(
        self,
        mode={},
        model={},
        trainer={},
        distributed={},
        dataloader={}
    ):
        ...

    def create(self, config: FederateConfig):
        model = create(config.model.name, config.mode.args)
        trainer = create(config.trainer.name, config.trainer.args, model)
        distributor = create(config.distributed.name, config.distributed.args)
        server_or_client = create(config.mode.name, config.mode.args)
        data_loader = create(config.dataloader.name, config.dataloader.args)
        manager = Manager(server_or_client, model, trainer, distributor)
        return manager

def create(*args):
    ...


federate_facotry = FederateFactory()

fed_configs = {}
fed_runs = {}

@app.post("/create_federation")
def create_federation(config: FederateConfig):
    manager = federate_facotry(config)
    fed_configs[0] = config
    fed_runs[0] = {"id": 0, "config": config}
    return 0


@app.post("/federated")
def join_federation(request: Request, run_id: int):
    def create_token(run_id, device):
        return "xxxx"

    dic = fed_runs[run_id]
    id = dic["id"]
    config = dic["config"]
    token = create_token(run_id, request["device"])
    return token
