import os
import subprocess
import tempfile
import time
from celery import Celery, current_task
from ai_agent import analyze_code
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Optional

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)


def clone_repository(repo_url, repo_dir, token=None, retries=3):
    if token:
        # Embed token in the repo URL for authentication
        repo_url = repo_url.replace("https://", f"https://{token}@")
    for attempt in range(retries):
        try:
            subprocess.run(['git', 'config', '--global', 'http.postBuffer', '524288000'], check=True)
            subprocess.run(['git', 'clone', '--depth', '1', repo_url, repo_dir], check=True)
            return
        except subprocess.CalledProcessError:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise

@celery_app.task
def analyze_pr_task(repo_url, pr_number, github_token=None):
    os.chdir('/tmp')

    with tempfile.TemporaryDirectory() as repo_dir:
        # Clone the repository with retries and optional token
        clone_repository(repo_url, repo_dir, token=github_token)
        os.chdir(repo_dir)

        # Fetch PR and checkout
        subprocess.run(['git', 'fetch', 'origin', f'pull/{pr_number}/head:pr-{pr_number}'], check=True)
        subprocess.run(['git', 'checkout', f'pr-{pr_number}'], check=True)

        # Collect .py files
        code_files = []
        for root, _, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        code_content = f.read()
                    code_files.append({
                        'file_name': os.path.relpath(file_path, repo_dir),  # Relative path for clarity
                        'code': code_content
                    })

        # Retrieve the current task's ID
        task_id = current_task.request.id  # Obtain Celery's task ID

        # Analyze code with task_id
        results = analyze_code(code_files, task_id=task_id)  # Pass task_id to analyze_code
        return results