# tests/test_tasks.py

import pytest
import subprocess 
from tasks import clone_repository, analyze_pr_task
import ai_agent

def test_clone_repository_success(monkeypatch):
    def mock_run(*args, **kwargs):
        pass  # Simulate successful git clone

    monkeypatch.setattr(subprocess, 'run', mock_run)
    
    try:
        clone_repository("https://github.com/instructlab/training.git", "/tmp/repo")
    except Exception:
        pytest.fail("clone_repository raised an exception unexpectedly!")

def test_analyze_pr_task(monkeypatch):
    # Mock the analyze_code function to return a predictable result
    def mock_analyze_code(code_files):
        # Return a list of dictionaries with 'name' and 'issues' keys
        return {
            "files": [
                {
                    "name": "main.py",
                    "issues": [
                        {
                            "type": "style",
                            "line": 15,
                            "description": "Line too long",
                            "suggestion": "Break line into multiple lines"
                        },
                        {
                            "type": "bug",
                            "line": 23,
                            "description": "Potential null pointer",
                            "suggestion": "Add null check"
                        }
                    ]
                }
            ],
            "summary": {
                "total_files": 1,
                "total_issues": 2,
                "critical_issues": 1
            }
        }
    
    # Correctly patch 'ai_agent.analyze_code'
    
    monkeypatch.setattr(ai_agent, 'analyze_code', mock_analyze_code)

    # Mock subprocess.run to avoid actual git commands during testing
    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: None)

    repo_url = "https://github.com/instructlab/training.git"
    pr_number = 1
    github_token = "optional_token"

def test_analyze_pr_task_with_invalid_analyze_code(monkeypatch):
    # Mock the analyze_code function to return an incorrect structure
    def mock_analyze_code(code_files):
        # Return a list of strings instead of the expected dictionary
        return "This is an invalid response"
    
    # Patch 'ai_agent.analyze_code' with the invalid mock
    monkeypatch.setattr(ai_agent, 'analyze_code', mock_analyze_code)

    # Mock subprocess.run to avoid actual git commands during testing
    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: None)

    repo_url = "https://github.com/user/repo.git"
    pr_number = 123
    github_token = "optional_token"

    # Invoke the task synchronously for testing
    result = analyze_pr_task(repo_url, pr_number, github_token)
