from app.vector_store.chroma import search, list_collections
from app.config import settings

def retrieve(question, document_ids=None):
    doc_ids = document_ids or list_collections()

    if not doc_ids:
        return []
    
    results = search(
        question=question,
        document_ids=doc_ids,
        top_k=settings.TOP_K
    )
    return results

def retrieve_with_scores(question, document_ids=None, score_threshold=1.5):
    results = retrieve(question, document_ids)
    return [r for r in results if r['score'] <= score_threshold]