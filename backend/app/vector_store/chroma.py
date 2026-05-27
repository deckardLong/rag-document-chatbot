import chromadb
from app.config import settings 
from app.vector_store.base import BaseVectorStore
from app.core.embedder import embed_documents, embed_query

_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

def get_collection(document_id):
    return _client.get_or_create_collection(name=document_id)

def add_chunks(document_id, chunks):
    collection = get_collection(document_id)
    embeddings = embed_documents(chunks)
    ids = [f'{document_id}_{i}' for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def search(question, document_ids, top_k):
    q_embedding = embed_query(question)
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

class ChromaVectorStore(BaseVectorStore):
    def __init__(self):
        self.client = _client
    
    def add_chunks(self, document_id, chunks):
        add_chunks(document_id, chunks)
    
    def search(self, question, document_ids, top_k):
        return search(question, document_ids, top_k)
    
    def list_collections(self):
        return list_collections()
    
    def delete_collection(self, document_id):
        delete_collection(document_id)