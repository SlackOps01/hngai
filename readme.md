# 🤖 Cybersecurity Summarizer Agent

A FastAPI-based A2A (Agent-to-Agent) compliant agent that scrapes and summarizes cybersecurity news from The Hacker News.

## 📋 Overview

- **Project Type**: FastAPI Web Application
- **Architecture**: A2A (Agent-to-Agent) Compliant
- **Primary Function**: Cybersecurity news summarization via web scraping and AI
- **Target Audience**: Security professionals, DevOps teams, automation platforms
- **Protocol**: JSON-RPC 2.0 compliant

## 🚀 Features

- 🔗 **A2A Protocol Compliance**: Fully compliant with Agent-to-Agent communication standards
- 📰 **Real-time Scraping**: Automatically fetches latest cybersecurity headlines from The Hacker News
- 🧠 **AI-Powered Summarization**: Uses OpenRouter API for intelligent text summarization
- 🌐 **RESTful API**: Clean HTTP endpoints with JSON-RPC 2.0 support
- 🔄 **Auto-Generation**: Automatic task, message, and artifact creation
- 🛡️ **Error Handling**: Comprehensive error handling and logging
- 🔍 **Discovery Endpoint**: A2A discovery endpoint for agent registration

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **Web Scraping**: BeautifulSoup4, Requests, lxml
- **AI/ML**: OpenRouter API (meta-llama/llama-3.3-8b-instruct:free)
- **Data Validation**: Pydantic
- **Server**: Uvicorn
- **Environment**: python-dotenv

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- OpenRouter API key (free at https://openrouter.ai/)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cybersecurity-summarizer-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```
   API_KEY=your_openrouter_api_key_here
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🚀 Usage

### Running the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Accessing the Application

- **API Documentation**: http://localhost:8000/docs
- **A2A Discovery**: http://localhost:8000/.well-known/a2a.json
- **Main Endpoint**: http://localhost:8000/

## 📚 API Documentation

### A2A Protocol Support

This agent implements the A2A (Agent-to-Agent) protocol with JSON-RPC 2.0 compliance:

- **Task Management**: Automatic task creation and status tracking
- **Message Handling**: Structured message passing with roles and content
- **Artifact Generation**: Automatic creation of summary artifacts

### API Endpoints

#### 1. Main A2A Endpoint
- **Method**: `POST`
- **Path**: `/`
- **Description**: Main Telex-compatible entrypoint for agent communication

#### 2. A2A Discovery Endpoint
- **Method**: `GET`
- **Path**: `/.well-known/a2a.json`
- **Description**: Agent discovery and metadata endpoint

### Request/Response Examples

#### A2A Discovery Response
```json
{
  "name": "CybersecuritySummarizerAgent",
  "version": "1.0.0",
  "a2a_version": "1.0",
  "description": "An AI agent that scrapes and summarizes cybersecurity headlines.",
  "endpoints": {"invoke": "/"},
  "inputs": {},
  "outputs": {
    "summary": {
      "type": "string",
      "description": "Summarized cybersecurity headlines."
    }
  }
}
```

#### Main Endpoint Response
```json
{
  "jsonrpc": "2.0",
  "id": "uuid-string",
  "result": {
    "id": "task-uuid",
    "contextId": "ctx-uuid",
    "status": {
      "state": "completed",
      "timestamp": "2025-01-01T00:00:00.000Z",
      "message": {
        "kind": "message",
        "role": "agent",
        "parts": [
          {
            "kind": "text",
            "text": "📰 Cybersecurity Summary:\n\n- Summary content here...",
            "data": null,
            "file_url": null
          }
        ],
        "messageId": "msg-uuid",
        "taskId": "task-uuid",
        "metadata": null
      }
    },
    "artifacts": [
      {
        "artifactId": "artifact-uuid",
        "name": "CybersecuritySummary",
        "parts": [
          {
            "kind": "text",
            "text": "📰 Cybersecurity Summary:\n\n- Summary content here...",
            "data": null,
            "file_url": null
          }
        ]
      }
    ],
    "history": [...],
    "kind": "task"
  },
  "error": null
}
```

### cURL Examples

#### Test the Main Endpoint
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Get A2A Discovery Information
```bash
curl http://localhost:8000/.well-known/a2a.json
```

## 🏗️ Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic models for data validation
│   └── summarizer.py    # Core summarization logic and web scraping
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not committed)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Key Components

#### [`app/main.py`](app/main.py:1)
- FastAPI application setup
- A2A-compliant endpoint handlers
- JSON-RPC 2.0 response formatting
- Error handling and logging

#### [`app/summarizer.py`](app/summarizer.py:1)
- Web scraping logic for The Hacker News
- AI summarization using OpenRouter API
- Content processing and headline extraction

#### [`app/models.py`](app/models.py:1)
- Pydantic models for data validation
- A2A protocol data structures
- Message and artifact models

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | OpenRouter API key for AI summarization | Yes |

### Model Configuration

The agent uses the following AI model for summarization:
- **Current Model**: `meta-llama/llama-3.3-8b-instruct:free`
- **Alternative Models** (faster options):
  - `gpt-4o-mini`
  - `claude-3-haiku`
  - `mistral-small`

To change the model, modify the `model` parameter in [`app/summarizer.py:34`](app/summarizer.py:34).

## 🧪 Development

- **Async Support**: Built with FastAPI's async capabilities for performance



### Documentation

- API Documentation: http://localhost:8000/docs
- OpenRouter Documentation: https://openrouter.ai/docs
- FastAPI Documentation: https://fastapi.tiangolo.com/


