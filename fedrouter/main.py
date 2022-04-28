from fastapi import FastAPI, HTTPException
from typing import Any, Optional, Dict


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


app = FastAPI()


def get_external_url():
    return "http://111.111.111.111"


def publish_domain_id():
    import random

    return random.randint()


def parse_url(url: str):
    from urllib.parse import urlparse

    obj = urlparse(url)

    if obj.port is None:
        if obj.scheme == "http":
            obj.port = 80
        elif obj.scheme == "https":
            obj.port = 443
        else:
            raise AppException()

    return obj


@app.get("/")
def get_me():
    return {"id": 1, "url": get_external_url()}


@app.get("/domain/get_central")
def get_central_domain():
    me = get_me()
    return me


@app.get("/domain/query")
def query_domain():
    me = get_me()
    return [me]


@app.post("/domain/add")
def add_domain(*, url: str):

    obj = parse_url(url)
    return {"id": publish_domain_id(), "url": obj.geturl()}


@app.post("/domain/approve")
def approve_domain(domain_id):
    ...


@app.get("/worker/get_accese_token")
def get_accese_token_for_worker(description: str):
    ...


@app.post("/security/create_global")
def create_global_security(group_name: str, domain_ids: list = None):
    ...


@app.post("/security/create")
def create_security(group_name: str, domain_ids: list = None):
    ...


@app.post("/group/create")
def create_group(group_name: str, domain_ids: list = None):
    ...


@app.get("/worker/create")
def create_executor(group_id: str, topology_type: str = None):
    ...


@app.get("/job/create")
def create_job():
    ...


@app.get("/run/create")
def create_run(job_id: str, executor_id: str):
    ...


@app.post("/run/create")
def start_run(run_id: str):
    ...


@app.post("/run/create")
def stop_run(run_id: str):
    ...


@app.get("/model/get")
def get_model(model):
    ...


@app.post("/model/push")
def push_model(model):
    ...


@app.get("/model/pull")
def pull_model(model_id: int, hash: str = None):
    if hash is None:
        return ""


@app.get("/model/list")
def list_model(model):
    ...


@app.post("/dataset/push")
def push_dataset(model):
    ...


@app.get("/dataset/pull")
def pull_dataset(dataset_id: int, hash: str = None):
    if hash is None:
        return ""


@app.get("/topology/analyze")
def analyze_topology(group_id: str = None, group_name: str = None):
    ...
