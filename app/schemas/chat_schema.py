from pydantic import BaseModel
from typing import Any, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    data: Optional[Any] = None
