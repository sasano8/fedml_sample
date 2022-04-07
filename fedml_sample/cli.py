import typer
from functools import wraps
import json


app = typer.Typer(no_args_is_help=True)


def run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p = func(*args, **kwargs)
        valid = validate(*p)
        s = json.dumps(valid)
        typer.echo(f"RUN: {s}")

    wrapper.__name__ = "run"
    return wrapper


def dry_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p = func(*args, **kwargs)
        valid = validate(*p)
        s = json.dumps(valid)
        typer.echo(f"{s}")

    wrapper.__name__ = "dry_run"
    return wrapper


def show_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p = func(*args, **kwargs)
        valid = validate(*p)
        module = valid["module"]
        mpi_params = valid["mpi_params"]
        params = valid["params"]

        s = f"mpirun -np {mpi_params['np']} -hostfile {mpi_params['hostfile']} python3 ./{module}"  # noqa
        p = " \\\n".join(f"--{k} {v}" for k, v in params.items())

        if p:
            s = s + " \\\n" + p

        typer.echo(f"{s}")

    wrapper.__name__ = "show_command"
    return wrapper


def validate(module, mpi_params, params):
    return {"module": module, "mpi_params": mpi_params, "params": params}


def split_mpi_params(params: dict):
    module = params.pop("module")

    mpi_params = {
        "hostfile": params.pop("hostfile", None),
        "np": params.pop("np", None),
    }
    return module, mpi_params, params


def xxx1(
    module: str = "main_fedgkt.py",
    hostfile: str = "mpi_host_file",
    np: int = 9,
    *,
    gpu: int = 1,
    dataset: str = "mydata.csv",
    round: int = 0,
    epoch_client: int = 0,
    epoch_server: int = 0,
    optm: int = 0,
    lr: int = 0,
    train_or_not: bool = True,
    distill_on_server: int = 0,
    client_mode: int = 0,
    name: str = "name",
    data_dir="./data",
    batch_size: int = 0,
):
    params = locals()
    return split_mpi_params(params)


def xxx2(
    module: str = "main_fedavg.py",
    # hostfile: str = "mpi_host_file",
    # np: int = 9,
    *,
    gpu: int = 1,
    dataset: str = "mydata.csv",
    data_dir="./data",
    model: str = "model_1",
    partition_method: str = "",
    client_num_in_total: int = 1,
    client_num_per_round: int = 1,
    comm_round: int = 1,
    epochs: int = 1,
    batch_size: int = 1,
    client_optimizer: str = "opt_1",
    lr: str = "",
    ci: str = "",
):
    params = locals()
    return split_mpi_params(params)


"""
sh run_fedavg_distributed_pytorch.sh \
    --client_num_in_total <client_num_in_total> \
    --client_num_per_round <client_num_per_round> \
    --model <model> \
    --partition_method <partition_method>
    --comm_round <comm_round> \
    --epochs <epochs>\
    --batch_size <batch_size> \
    --learning_rate <learning_rate> \
    --dataset <dataset> \
    --data_dir <data_dir> \
    --client_optimizer <client_optimizer> \
    --backend <backend> \
    --grpc_ipconfig_path <grpc_ipconfig_path> \
    --trpc_master_config_path\
    --ci <ci>

mpirun -np $ PROCESS_NUM -hostfile ./mpi_host_file python3 ./main_fedavg.py \
  --gpu_mapping_file " gpu_mapping.yaml " \
  --gpu_mapping_key " mapping_default " \
  --モデル$MODEL \
  --データセット$DATASET \
  --data_dir $ DATA_DIR \
  --partition_method $ DISTRIBUTION   \
  --client_num_in_total $ CLIENT_NUM \
  --client_num_per_round $ WORKER_NUM \
  --comm_round $ ROUND \
  --エポック$EPOCH \
  --client_optimizer $ CLIENT_OPTIMIZER \
  --batch_size $ BATCH_SIZE \
  --lr $ LR \
  --ci $ CI
"""


def grpc(module: str = "main_fedavg_rpc.py"):
    ...


cmd_1 = typer.Typer()
cmd_2 = typer.Typer(
    help="""https://github.com/FedML-AI/FedML/blob/master/fedml_experiments/standalone/fedavg/run_fedavg_standalone_pytorch.sh""",
)


cmd_1.command()(run(xxx1))
cmd_1.command()(dry_run(xxx1))
cmd_1.command()(show_command(xxx1))

cmd_2.command()(run(xxx2))
cmd_2.command()(dry_run(xxx2))
cmd_2.command()(show_command(xxx2))


app.add_typer(cmd_1, name="cmd_1")
app.add_typer(cmd_2, name="cmd_2")
