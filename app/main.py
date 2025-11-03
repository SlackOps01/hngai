from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from summarizer import summarize_articles

app = FastAPI(
    title="Cybersecurity Summarizer Agent",
    description="An A2A-compliant agent that scrapes and summarizes cybersecurity news.",
    version="1.0.0"
)

# ----------------------------
# .well-known A2A JSON (Discovery)
# ----------------------------
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
        "inputs": {
            "source_url": {
                "type": "string",
                "required": False,
                "default": "https://thehackernews.com/",
                "description": "The URL to scrape cybersecurity headlines from."
            }
        },
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
        "description": "Scrapes and summarizes cybersecurity headlines from a given URL.",
        "inputs": ["source_url"],
        "outputs": ["summary"]
    }

# ----------------------------
# A2A INVOKE ENDPOINT
# ----------------------------
class InvokeRequest(BaseModel):
    source_url: str | None = None

@app.post("/a2a/invoke")
def invoke_agent(request: InvokeRequest):
    try:
        summary = summarize_articles(request.source_url or "https://thehackernews.com/")
        return {
            "protocol": "A2A",
            "version": "1.0",
            "status": "success",
            "outputs": {"summary": summary}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": str(e)})

