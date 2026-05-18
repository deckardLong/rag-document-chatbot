from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.core.pipeline import run_rag

router = APIRouter()

@router.post('/chat', response_model=ChatResponse)
async def chat(request: ChatRequest):
    return run_rag(request)