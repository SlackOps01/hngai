from pydantic import BaseModel
from typing import Optional

class A2AContent(BaseModel):
    text: Optional[str]
    metadata: Optional[dict] = {}

class A2AMessage(BaseModel):
    protocol: str
    sender: str
    recipient: str
    type: str
    content: Optional[A2AContent]