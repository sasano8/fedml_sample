from fastapi import FastAPI, Query
from pydantic import Field
from typing import Literal

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

MODELS = Literal["rnn"]


@app.post("/fedml/fedavg")
def fedavg(
    *,
    gpu: int,
    dataset: str,
    data_dir: str,
    model: MODELS = "rnn",
    partition_method: str,
    client_num_in_total: int,
    client_num_per_round: int,
    comm_round: int = Query(1000, description="ラウンド数？"),
    batch_size: int = Query(..., description="データセットをいくつかに分割し、分割された塊の数"),
    epochs: int = Query(
        1,
        # description="It specifies the number of iterations. Epoch mean one complete pass of the training dataset through the algorithm."
        description="batch_sizeを元のデータセット分反復することを1エポック。通常数エポック実行する。",
    ),
    client_optimizer: str,
    lr: float = Query(..., description="学習率のこと？"),
    ci: int
):
    "${workspaceFolder}/fedml_experiments/standalone/fedavg"
