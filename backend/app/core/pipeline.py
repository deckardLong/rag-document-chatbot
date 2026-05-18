from app.vector_store.chroma import search, list_collections
from app.core.generator import generate_answer
from app.models.chat import ChatRequest, ChatResponse, Source
from app.config import settings

def run_rag(request: ChatRequest):
    doc_ids = request.document_ids or list_collections()

    if not doc_ids:
        return ChatResponse(answer='No documents have been uploaded yet.', sources=[])
    
    results = search(request.question, doc_ids, settings.TOP_K)

    if not results:
        return ChatResponse(answer='No relevant content found in the documents.', sources=[])
    
    chunks = [r['chunk'] for r in results]
    answer = generate_answer(request.question, chunks, request.chat_history or [])

    sources = [
        Source(document_id=r['document_id'], filename=r['document_id'], chunk=r['chunk'])
        for r in results
    ]
    return ChatResponse(answer=answer, sources=sources)