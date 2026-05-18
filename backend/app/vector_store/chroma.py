import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings 

_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def get_collection(document_id):
    return _client.get_or_create_collection(name=document_id)

def add_chunks(document_id, chunks):
    collection = get_collection(document_id)
    embeddings = _model.encode(chunks).tolist()
    ids = [f'{document_id}_{i}' for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def search(question, document_ids, top_k):
    q_embedding = _model.encode([question]).tolist()[0]
    results = []
    for doc_id in document_ids:
        try:
            col = get_collection(doc_id)
            res = col.query(query_embeddings=[q_embedding], n_results=top_k)
            for doc, dist in zip(res['documents'][0], res['distances'][0]):
                results.append({
                    'document_id': doc_id,
                    'chunk': doc,
                    'score': dist
                    })
        except Exception:
            continue
    results.sort(key=lambda x: x['score'])
    return results[:top_k]

def list_collections():
    return [c.name for c in _client.list_collections()]

def delete_collection(document_id):
    _client.delete_collection(document_id)