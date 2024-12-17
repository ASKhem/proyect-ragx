from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

    class Config:
        from_attributes = True  # Para compatibilidad con Pydantic v2

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: float = 0.5
    max_tokens: int = 1024

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[dict]] = None

class UploadResponse(BaseModel):
    message: str
    document_count: int
