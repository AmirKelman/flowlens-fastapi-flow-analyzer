from fastapi import FastAPI
from pydantic import BaseModel
from rq import Queue
from redis import Redis

app = FastAPI(title="FlowLens")

redis = Redis(host="localhost", port=6379)
queue = Queue("flowlens", connection=redis)


class Source(BaseModel):
    type: str
    value: str


class AnalyzeRequest(BaseModel):
    source: Source


@app.post("/analyze", status_code=202)
def analyze(req: AnalyzeRequest):
    repo_id = "demo-repo"  # TODO: generate stable id
    queue.enqueue("flowlens.worker.analyze_repo", repo_id, req.source.model_dump())
    return {"repo_id": repo_id, "status": "QUEUED"}


@app.get("/repos/{repo_id}/status")
def status(repo_id: str):
    # TODO: read from storage
    return {"repo_id": repo_id, "status": "QUEUED", "message": ""}
