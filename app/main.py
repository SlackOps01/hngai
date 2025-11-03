from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .summarizer import summarize_articles  # no relative import for uvicorn compatibility

app = FastAPI(
    title="Cybersecurity Summarizer Agent",
    description="An A2A-compliant agent that scrapes and summarizes cybersecurity news.",
    version="1.0.0"
)

# ----------------------------
# .well-known A2A JSON (Discovery)
# ----------------------------
@app.get("/")
def root():
    return {"message": "Cybersecurity Summarizer Agent active. See /.well-known/a2a.json"}

@app.post("/")
async def root_post(request: Request):
    """
    Fallback handler for systems (like Telex) that POST directly to root.
    We’ll redirect them to the A2A invoke logic.
    """
    try:
        summary = summarize_articles()
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "success",
                "outputs": {"summary": summary}
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "protocol": "A2A",
                "version": "1.0",
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )
    

@app.get("/.well-known/a2a.json")
def wellknown_a2a():
    """
    Discovery endpoint describing this AI Agent.
    """
    return {
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
    }

# ----------------------------
# A2A METADATA ENDPOINT
# ----------------------------
@app.get("/a2a/metadata")
def get_metadata():
    return {
        "name": "Cybersecurity Summarizer",
        "version": "1.0.0",
        "description": "Scrapes and summarizes cybersecurity headlines from The Hacker News.",
        "inputs": [],
        "outputs": ["summary"]
    }

# ----------------------------
# A2A INVOKE ENDPOINT
# ----------------------------
class InvokeRequest(BaseModel):
    # request body kept for A2A compliance, but unused
    source_url: str | None = None

@app.post("/a2a/invoke")
def invoke_agent(request: InvokeRequest):
    """
    Main A2A entrypoint. Ignores input and runs summarize_articles().
    """
    try:
        summary = summarize_articles()  # no arguments needed
        return {
            "protocol": "A2A",
            "version": "1.0",
            "status": "success",
            "outputs": {"summary": summary}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "message": str(e)
        })
