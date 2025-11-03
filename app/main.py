from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .summarizer import summarize_articles  # use absolute import if deploying

app = FastAPI(
    title="Cybersecurity Summarizer Agent",
    description="An A2A-compliant agent that scrapes and summarizes cybersecurity news.",
    version="1.0.0"
)

# ----------------------------
# Root and Fallback
# ----------------------------
@app.get("/")
def root():
    return {"message": "Cybersecurity Summarizer Agent active. See /.well-known/a2a.json"}

@app.post("/")
async def root_post():
    """
    Fallback for platforms like Telex that POST to root.
    """
    try:
        summary = summarize_articles()
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "success",
                "outputs": {"summary": summary}
            },
            media_type="application/json"
        )
    except Exception as e:
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "error",
                "message": str(e)
            },
            status_code=500,
            media_type="application/json"
        )

# ----------------------------
# Well-Known A2A Discovery
# ----------------------------
@app.get("/.well-known/a2a.json")
def wellknown_a2a():
    return JSONResponse(
        content={
            "name": "CybersecuritySummarizerAgent",
            "version": "1.0.0",
            "a2a_version": "1.0",
            "description": "An AI agent that scrapes and summarizes cybersecurity headlines.",
            "endpoints": {
                "metadata": "/a2a/metadata",
                "invoke": "/a2a/invoke"
            },
            "inputs": {},
            "outputs": {
                "summary": {
                    "type": "string",
                    "description": "Summarized cybersecurity headlines."
                }
            }
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
            "description": "Scrapes and summarizes cybersecurity headlines from The Hacker News.",
            "inputs": [],
            "outputs": ["summary"]
        },
        media_type="application/json"
    )

# ----------------------------
# A2A Invoke
# ----------------------------
class InvokeRequest(BaseModel):
    source_url: str | None = None  # unused

@app.post("/a2a/invoke")
async def invoke_agent(_: InvokeRequest):
    """
    A2A entrypoint that triggers the summarizer.
    """
    try:
        summary = summarize_articles()
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "success",
                "outputs": {"summary": summary}
            },
            media_type="application/json"
        )
    except Exception as e:
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "error",
                "message": str(e)
            },
            status_code=500,
            media_type="application/json"
        )
