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

MODELS = Literal["rnn", "resnet56"]
OPTIMIZERS = Literal["sgd", "adam"]
PARTITION_METHODS = Literal["hetero"]
DISTRIBUTIONS = Literal["homo", "lumo"]  # 満足がいくデータセットが得られない場合に、テストデータセットを予測し、データセットを補完する。

class MpiHost(BaseModel):
    """
    計算を実行する
    """

    host: str = Field(description="host名またはipを指定")
    slots: int = Field(description="CPU数を指定")

class MpiHostFile(BaseModel):
    """
    形式はバージョンにより２つある。
    node1:4
    node1 slots=4
    """
    __root__: List[MpiHost]


@app.post("/fedml/fedavg")
def create_mpi_host_file(mpi_host_file: MpiHostFile):
    return "\n".join(x.host + f":{x.slots}" for x in mpi_host_file.__root__)

@app.post("/fedml/fedavg")
def fedavg(
    *,
    gpu: int = Query(0, description=""),
    dataset: str,
    data_dir: str,
    model: MODELS = "rnn",
    partition_method: PARTITION_METHODS = Query("hetero", description="how to partition the dataset on local workers"),
    client_num_in_total: int,
    client_num_per_round: int,
    comm_round: int = Query(1000, description="how many round of communications we should use"),
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