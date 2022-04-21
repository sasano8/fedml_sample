from fastapi import FastAPI, Query
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
PARTITION_METHODS = Literal["hetero"]
DISTRIBUTIONS = Literal["homo", "lumo"]  # 満足がいくデータセットが得られない場合に、テストデータセットを予測し、データセットを補完する。

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
    MyModelTrainerTAG(model)
    MyModelTrainerNWP(model)
    MyModelTrainerCLS(model)



from typing import NamedTuple

class Discriminator(NamedTuple):
    name: str
    args: dict

class FederateConfig(BaseModel):
    aggregator: str
    model: Discriminator
    trainer: Discriminator

    class Config:
        schema_extra = {
            'examples': [
                {
                    "aggregator": "xxx.com",
                    "model": [
                        "LogisticRegression",
                        {
                            "input_dim": 1,
                            "output_dim": 1
                        }
                    ],
                    "trainer": [
                        "MyModelTrainerTAG",
                        {}
                    ]
                }
            ]
        }

@app.post("/federated")
def federated(config: FederateConfig):
    return config
