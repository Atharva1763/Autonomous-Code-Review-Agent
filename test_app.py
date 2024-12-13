import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_analyze_pr():
    payload = {
        "repo_url": "https://github.com/instructlab/training.git",
        "pr_number": 1
    }
    response = client.post("/analyze-pr", json=payload)
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_get_status():
    task_id = "dummy_task_id"
    response = client.get(f"/status/{task_id}")
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id

def test_get_results_not_ready():
    task_id = "dummy_task_id"
    response = client.get(f"/results/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Result not ready"