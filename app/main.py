from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from .summarizer import summarize_articles  # use absolute import if deploying

app = FastAPI(
    title="Cybersecurity Summarizer Agent",
    description="An A2A-compliant agent that scrapes and summarizes cybersecurity news.",
    version="1.0.0"
)

# ----------------------------
# Temporary in-memory store
# ----------------------------
TASK_RESULTS = {}

# ----------------------------
# Root + fallback for Telex
# ----------------------------
@app.get("/")
def root():
    return {"message": "Cybersecurity Summarizer Agent active. See /.well-known/a2a.json"}

@app.post("/")
async def root_post(background_tasks: BackgroundTasks):
    """
    Handles Telex POST directly to root.
    """
    task_id = str(uuid.uuid4())

    # Schedule background summarization
    background_tasks.add_task(run_summary_background, task_id)

    return JSONResponse(
        content={
            "protocol": "A2A",
            "version": "1.0",
            "status": "processing",
            "message": "Summarization started. Fetch results from /a2a/result/{task_id}",
            "task_id": task_id
        },
        media_type="application/json"
    )

# ----------------------------
# Background job
# ----------------------------
def run_summary_background(task_id: str):
    try:
        summary = summarize_articles()
        TASK_RESULTS[task_id] = {
            "status": "success",
            "summary": summary
        }
    except Exception as e:
        TASK_RESULTS[task_id] = {
            "status": "error",
            "message": str(e)
        }

# ----------------------------
# A2A Discovery
# ----------------------------
@app.get("/.well-known/a2a.json")
def wellknown_a2a():
    return JSONResponse(
        content={
            "name": "CybersecuritySummarizerAgent",
            "version": "1.0.0",
            "a2a_version": "1.0",
            "description": "An AI agent that scrapes and summarizes cybersecurity headlines asynchronously.",
            "endpoints": {
                "metadata": "/a2a/metadata",
                "invoke": "/a2a/invoke",
                "result": "/a2a/result/{task_id}"
            },
            "inputs": {},
            "outputs": {
                "summary": {
                    "type": "string",
                    "description": "Summarized cybersecurity headlines."
                }
            },
            "notes": "After invoking, poll /a2a/result/{task_id} for the finished summary."
        },
        media_type="application/json"
    )

# ----------------------------
# A2A Metadata
# ----------------------------
@app.get("/a2a/metadata")
def get_metadata():
    return JSONResponse(
        content={
            "name": "Cybersecurity Summarizer",
            "version": "1.0.0",
            "description": (
                "Scrapes and summarizes cybersecurity headlines from The Hacker News. "
                "This agent runs asynchronously — fetch results via /a2a/result/{task_id}."
            ),
            "inputs": [],
            "outputs": ["summary"]
        },
        media_type="application/json"
    )

# ----------------------------
# A2A Invoke
# ----------------------------
class InvokeRequest(BaseModel):
    source_url: str | None = None

@app.post("/a2a/invoke")
async def invoke_agent(_: InvokeRequest, background_tasks: BackgroundTasks):
    """
    Main A2A entrypoint that starts summarization in the background.
    """
    task_id = str(uuid.uuid4())
    background_tasks.add_task(run_summary_background, task_id)

    return JSONResponse(
        content={
            "protocol": "A2A",
            "version": "1.0",
            "status": "processing",
            "message": "Summarization started. Fetch results from /a2a/result/{task_id}",
            "task_id": task_id
        },
        media_type="application/json"
    )

# ----------------------------
# A2A Result
# ----------------------------
@app.get("/a2a/result/{task_id}")
def get_result(task_id: str):
    """
    Returns the summary result for a given task_id.
    """
    result = TASK_RESULTS.get(task_id)
    if not result:
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "processing",
                "message": "Result not ready yet. Please check back later."
            },
            status_code=202,
            media_type="application/json"
        )

    return JSONResponse(
        content={
            "protocol": "A2A",
            "version": "1.0",
            **result
        },
        media_type="application/json"
    )
