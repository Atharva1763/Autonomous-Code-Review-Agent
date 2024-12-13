from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks import analyze_pr_task, celery_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# FastAPI Configuration
FASTAPI_HOST = os.getenv('FASTAPI_HOST', '127.0.0.1')
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT', 8000))

app = FastAPI()

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: str = None  # Optional token

@app.post("/analyze-pr")
def analyze_pr(request: AnalyzePRRequest):
    task = analyze_pr_task.delay(
        request.repo_url,
        request.pr_number,
        request.github_token
    )
    return {"task_id": task.id}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == 'PENDING':
        return {"task_id": task_id, "status": result.state}
    elif result.state != 'FAILURE':
        return {"task_id": task_id, "status": result.state}
    else:
        error = str(result.info)
        raise HTTPException(status_code=500, detail=error)

@app.get("/results/{task_id}")
def get_results(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        return {"task_id": task_id, "result": result.result}
    else:
        raise HTTPException(status_code=404, detail="Result not ready")