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
   # For OpenAI
   OPENAI_API_KEY=your_openai_api_key
   ```

   **Notes:**

   - **OpenAI Integration**: If you're using OpenAI's API, ensure you set the `OPENAI_API_KEY`.

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


### GET `/results/{task_id}`

**Description**: Retrieve the results of a completed analysis task.

**Path Parameters**:

- `task_id` (string): The unique identifier of the task.

**Response**:

- **If Completed Successfully**:

  ```json
{
  "results": {
    "style": [
      {
        "line_number": 7,
        "issue": "Imports are not grouped by standard libraries, third-party libraries, and local application imports.",
        "suggestion": "Group imports into three sections: standard libraries, third-party libraries, and local imports."
      },
    ],
    "bug": [
      {
        "line_number": 78,
        "issue": "Potential issue with hardcoded 'flash_attention_2' argument.",
        "suggestion": "Verify if 'flash_attention_2' is a valid option for the 'attn_implementation' parameter."
      },
    ],
    "performance": [
      {
        "line_number": 109,
        "issue": "Commented out 'torch.compile(model)' which can improve performance.",
        "suggestion": "Consider enabling 'torch.compile' for potential performance improvement."
      },
    ],
    "best_practice": [
      {
        "line_number": 57,
        "issue": "Direct exit using 'sys.exit' is not recommended.",
        "suggestion": "Use exception handling to exit the program gracefully."
      },
    ]
  }
}
```  ```

- **If Result Not Ready**:

  ```json
  {
    "detail": "Result not ready"
  }
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
========================= test session starts ==========================
platform linux -- Python 3.9.16, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/navcore/Desktop/ML/TakeHomeProject
plugins: anyio-3.7.1
collected 6 items                                                      

test_app.py ...                                                  [ 50%]
test_tasks.py ...                                                [100%]

========================== 6 passed in 1.25s ===========================
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

