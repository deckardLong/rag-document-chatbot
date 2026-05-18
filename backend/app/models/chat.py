from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class Source(BaseModel):
    document_id: str
    filename: str
    chunk: str

class ChatRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None
    chat_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]