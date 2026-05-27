from app.core.retriever import retrieve_with_scores, retrieve
from app.core.generator import generate_answer
from app.vector_store.chroma import list_collections
from app.models.chat import ChatRequest, ChatResponse, Source

def run_rag(request: ChatRequest):
    doc_ids = request.document_ids or list_collections()

    if not doc_ids:
        return ChatResponse(answer='No documents have been uploaded yet.', sources=[])
    
    results = retrieve_with_scores(question=request.question, document_ids=doc_ids, score_threshold=1.5)

    if not results:
        results = retrieve(request.question, doc_ids)

    if not results:
        return ChatResponse(answer='No relevant content found in the documents.', sources=[])
    
    chunks = [r['chunk'] for r in results]
    answer = generate_answer(question=request.question, 
                             context_chunks=chunks, 
                             chat_history=request.chat_history or [])

    sources = [
        Source(document_id=r['document_id'], filename=r['document_id'], chunk=r['chunk'])
        for r in results
    ]
    return ChatResponse(answer=answer, sources=sources)