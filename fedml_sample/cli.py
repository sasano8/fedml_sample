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
        mpi_params = valid["mpi_params"]
        params = valid["params"]

        s = f"mpirun -np {mpi_params['np']} -hostfile {mpi_params['hostfile']} python3 ./{mpi_params['module']}"  # noqa
        p = " \\\n".join(f"--{k} {v}" for k, v in params.items())

        if p:
            s = s + " \\\n" + p

        typer.echo(f"{s}")

    wrapper.__name__ = "show_command"
    return wrapper


def validate(mpi_params, params):
    return {"mpi_params": mpi_params, "params": params}


def split_mpi_params(params: dict):
    mpi_params = {
        "module": params.pop("module"),
        "hostfile": params.pop("hostfile"),
        "np": params.pop("np"),
    }
    return mpi_params, params


def create(
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


app.command()(run(create))
app.command()(dry_run(create))
app.command()(show_command(create))


# @app.command()
# def delete(item: str):
#     typer.echo(f"Deleting item: {item}")


# @app.command()
# def sell(item: str):
#     typer.echo(f"Selling item: {item}")
