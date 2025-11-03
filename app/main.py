import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .summarizer import summarize_articles  # local summarizer logic

app = FastAPI(
    title="Cybersecurity Summarizer Agent",
    description="An A2A-compliant agent that scrapes and summarizes cybersecurity news.",
    version="1.0.0"
)

# -------------------------------------------------
# Helper for timestamps
# -------------------------------------------------
def now_iso():
    return datetime.now(timezone.utc).isoformat()

# -------------------------------------------------
# Root and fallback POST (Telex calls this)
# -------------------------------------------------
@app.post("/")
async def root_post(_: Request):
    """
    Main Telex-compatible entrypoint.
    """
    try:
        summary = summarize_articles()

        task_id = f"task-{uuid.uuid4()}"
        context_id = f"ctx-{uuid.uuid4()}"
        message_id = f"msg-{uuid.uuid4()}"
        artifact_id = f"artifact-{uuid.uuid4()}"

        response = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "result": {
                "id": task_id,
                "contextId": context_id,
                "status": {
                    "state": "completed",
                    "timestamp": now_iso(),
                    "message": {
                        "kind": "message",
                        "role": "agent",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"📰 Cybersecurity Summary:\n\n{summary}",
                                "data": None,
                                "file_url": None
                            }
                        ],
                        "messageId": message_id,
                        "taskId": task_id,
                        "metadata": None
                    }
                },
                "artifacts": [
                    {
                        "artifactId": artifact_id,
                        "name": "CybersecuritySummary",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"📰 Cybersecurity Summary:\n\n{summary}",
                                "data": None,
                                "file_url": None
                            }
                        ]
                    }
                ],
                "history": [
                    {
                        "kind": "message",
                        "role": "user",
                        "parts": [{"kind": "text", "text": "", "data": None, "file_url": None}],
                        "messageId": f"msg-{uuid.uuid4()}",
                        "taskId": None,
                        "metadata": None
                    },
                    {
                        "kind": "message",
                        "role": "agent",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"📰 Cybersecurity Summary:\n\n{summary}",
                                "data": None,
                                "file_url": None
                            }
                        ],
                        "messageId": message_id,
                        "taskId": task_id,
                        "metadata": None
                    }
                ],
                "kind": "task"
            },
            "error": None
        }

        return JSONResponse(content=response)

    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "error": {
                "code": -32000,
                "message": "Internal Server Error",
                "data": str(e)
            }
        }
        return JSONResponse(content=error_response, status_code=500)

# -------------------------------------------------
# Well-known (A2A discovery)
# -------------------------------------------------
@app.get("/.well-known/a2a.json")
def wellknown_a2a():
    return JSONResponse(
        content={
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
    )
