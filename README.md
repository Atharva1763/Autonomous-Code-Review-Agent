# Autonomous Code Review Agent

## Table of Contents

- Introduction
- Features
- Technical Requirements
- Project Setup
  - Prerequisites
  - Installation
  - Configuration
- Running the Application
  - Start Redis Server
  - Start Celery Worker
  - Run FastAPI App
- API Documentation
  - POST `/analyze-pr`
  - GET `/status/{task_id}`
  - GET `/results/{task_id}`
- Design Decisions
- Future Improvements
- Testing
  - Running Tests
- Environment Variables
- License
- Acknowledgements
- Contact

## Introduction

The **Autonomous Code Review Agent** is a system designed to automate the analysis of GitHub pull requests (PRs). Leveraging AI capabilities, it performs comprehensive code reviews by checking for code style issues, potential bugs, performance improvements, and adherence to best practices. The system is built using modern Python frameworks and tools, ensuring scalability, reliability, and ease of use.

## Features

- **Automated PR Analysis**: Analyze GitHub pull requests for various code quality metrics.
- **Asynchronous Processing**: Utilize Celery for handling tasks asynchronously, ensuring non-blocking operations.
- **AI-Powered Insights**: Integrate with language models (e.g., OpenAI, Ollama) to provide in-depth code analysis.
- **Task Identification**: Each analysis task is assigned a unique `task_id` for tracking and result retrieval.
- **API Integration**: Interact seamlessly with developers through a structured FastAPI-based API.
- **Scalable Architecture**: Designed to handle multiple analyses concurrently with Redis as the message broker and result backend.

## Technical Requirements

- **Programming Language**: Python 3.8+
- **Web Framework**: FastAPI
- **Task Queue**: Celery
- **Message Broker & Backend**: Redis or PostgreSQL
- **AI Integration**: Any LLM API (e.g., OpenAI) or Ollama for local model execution
- **Testing Framework**: pytest

## Project Setup

### Prerequisites

Ensure you have the following installed on your system:

- **Python**: Version 3.8 or higher
- **Redis**: If opting for Redis as the message broker and backend
- **Git**: For cloning repositories
- **Ollama** (Optional): If you prefer running language models locally

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/autonomous-code-review-agent.git
   cd autonomous-code-review-agent
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Environment Variables**

   Create a `.env` file based on the provided `.env.example` to configure your environment variables.

   ```bash
   cp .env.example .env
   ```

   **`.env.example`**

   ```ini
   # FastAPI settings
   FASTAPI_HOST=127.0.0.1
   FASTAPI_PORT=8000

   # Celery settings
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0

   # AI Settings
   # Choose either OpenAI or Ollama

   # For OpenAI
   OPENAI_API_KEY=your_openai_api_key

   # For Ollama
   # OLLAMA_MODEL_NAME=your_ollama_model
   ```

   **Notes:**

   - **OpenAI Integration**: If you're using OpenAI's API, ensure you set the `OPENAI_API_KEY`.
   - **Ollama Integration**: If you prefer running language models locally with Ollama, set the `OLLAMA_MODEL_NAME` and ensure Ollama is installed and running.

2. **Apply Environment Variables**

   Ensure your environment variables are loaded. You can use packages like `python-dotenv` or manually export them.

   ```bash
   export $(cat .env | xargs)
   ```

## Running the Application

Follow the steps below to start the application components.

### Start Redis Server

If you're using Redis as the message broker and result backend:

```bash
redis-server
```

> **Note**: Ensure Redis is running on `localhost` with the default port `6379`. Adjust the `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in `.env` if Redis is running elsewhere.

### Start Celery Worker

Open a new terminal window/tab, activate the virtual environment, and start the Celery worker:

```bash
source venv/bin/activate
celery -A tasks.celery_app worker --loglevel=info
```

> **Note**: Ensure that 

tasks.py

 correctly defines `celery_app`.

### Run FastAPI App

In another terminal window/tab, activate the virtual environment, and start the FastAPI application:

```bash
source venv/bin/activate
uvicorn app:app --reload
```

- Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

## API Documentation

### POST `/analyze-pr`

**Description**: Initiate the analysis of a GitHub Pull Request.

**Request Body**:

```json
{
  "repo_url": "https://github.com/user/repo.git",
  "pr_number": 123,
  "github_token": "optional_token"  // Optional for private repositories
}
```

- `repo_url` (string): The URL of the GitHub repository.
- `pr_number` (integer): The pull request number to analyze.
- `github_token` (string, optional): A GitHub token if the repository is private or requires authentication.

**Response**:

```json
{
  "task_id": "abc123"
}
```

- `task_id` (string): The unique identifier for the analysis task.

**Example**:

```bash
curl -X POST "http://localhost:8000/analyze-pr" \
     -H "Content-Type: application/json" \
     -d '{
           "repo_url": "https://github.com/user/repo.git",
           "pr_number": 123
         }'
```

### GET `/status/{task_id}`

**Description**: Check the status of an ongoing analysis task.

**Path Parameters**:

- `task_id` (string): The unique identifier of the task.

**Response**:

```json
{
  "task_id": "abc123",
  "status": "PENDING" // or "SUCCESS", "FAILURE", etc.
}
```

**Example**:

```bash
curl -X GET "http://localhost:8000/status/abc123"
```

### GET `/results/{task_id}`

**Description**: Retrieve the results of a completed analysis task.

**Path Parameters**:

- `task_id` (string): The unique identifier of the task.

**Response**:

- **If Completed Successfully**:

  ```json
  {
    "task_id": "abc123",
    "status": "completed",
    "results": {
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
  }
  ```

- **If Result Not Ready**:

  ```json
  {
    "detail": "Result not ready"
  }
  ```

**Example**:

```bash
curl -X GET "http://localhost:8000/results/abc123"
```

## Testing

### Running Tests

The project uses `pytest` for testing. Follow the steps below to run the test suite.

1. **Ensure `pytest` is Installed**

   If not already installed, install `pytest`:

   ```bash
   pip install pytest
   ```

2. **Navigate to the Project Root**

   ```bash
   cd autonomous-code-review-agent
   ```

3. **Run Tests**

   ```bash
   pytest
   ```

   **Expected Output**:

   ```
   ============================= test session starts ==============================
   platform linux -- Python 3.9.7, pytest-7.1.2, pluggy-1.0.0
   rootdir: /path/to/autonomous-code-review-agent
   collected 4 items

   tests/test_tasks.py ....                                               [100%]

   ============================== 4 passed in 0.12s ===============================
   ```

### Test Coverage

To check test coverage, install `pytest-cov`:

```bash
pip install pytest-cov
```

Run tests with coverage report:

```bash
pytest --cov=.
```

**Example Output**:

```
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-7.1.2, pluggy-1.0.0
rootdir: /path/to/autonomous-code-review-agent
plugins: cov-3.0.0
collected 4 items

tests/test_tasks.py ....                                               [100%]

---------- coverage: platform linux, python 3.9.7-final-0 -----------
Name                   Stmts   Miss  Cover
----------------------------------------
tasks.py                   60      3    95%
ai_agent.py               40      0   100%
app.py                    50      2    96%
----------------------------------------
TOTAL                     150      5    97%

============================== 4 passed in 0.15s ===============================
```

## Environment Variables

The application uses environment variables for configuration. Below is the `.env.example` file outlining the necessary variables.

**`.env.example`**

```ini
# FastAPI settings
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000

# Celery settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI Settings
# Choose either OpenAI or Ollama

# For OpenAI
OPENAI_API_KEY=your_openai_api_key

# For Ollama
# OLLAMA_MODEL_NAME=your_ollama_model
```

**Instructions**:

1. **Copy the Example File**

   ```bash
   cp .env.example .env
   ```

2. **Set Environment Variables**

   Open `.env` and set the appropriate values:

   - **FastAPI Host and Port**: Update if you want to run the API on a different host or port.
   - **Celery Broker and Backend**: Ensure Redis URLs are correct.
   - **AI Integration**:
     - **OpenAI**: Set `OPENAI_API_KEY` if using OpenAI's API.
     - **Ollama**: Uncomment and set `OLLAMA_MODEL_NAME` if using Ollama.

3. **Load Environment Variables**

   You can use `python-dotenv` or manually export variables:

   ```bash
   export $(cat .env | xargs)
   ```

### Example Workflow

1. **Initiate Analysis**

   Send a POST request to `/analyze-pr` with the repository URL and PR number.

   **Request**:

   ```json
   {
     "repo_url": "https://github.com/user/repo.git",
     "pr_number": 123
   }
   ```

   **Response**:

   ```json
   {
     "task_id": "3d4544f6-75ba-433a-a4f7-4aa0870dbfdc"
   }
   ```

2. **Check Task Status**

   Use the provided `task_id` to check the status.

   **Request**:

   ```bash
   GET /status/3d4544f6-75ba-433a-a4f7-4aa0870dbfdc
   ```

   **Response**:

   ```json
   {
     "task_id": "3d4544f6-75ba-433a-a4f7-4aa0870dbfdc",
     "status": "COMPLETED" // Possible values: PENDING, STARTED, SUCCESS, FAILURE
   }
   ```

3. **Retrieve Analysis Results**

   Once the task status is `COMPLETED`, retrieve the results.

   **Request**:

   ```bash
   GET /results/3d4544f6-75ba-433a-a4f7-4aa0870dbfdc
   ```

   **Response**:

   ```json
   {
     "task_id": "3d4544f6-75ba-433a-a4f7-4aa0870dbfdc",
     "status": "completed",
     "results": {
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
   }
   ```
