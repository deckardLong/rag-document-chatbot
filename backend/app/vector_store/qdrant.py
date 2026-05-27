from app.vector_store.base import BaseVectorStore
from app.core.embedder import embed_documents, embed_query

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

VECTOR_SIZE = 768

class QdrantVectorStore(BaseVectorStore):
    def __init__(self, url='http://localhost:6333'):
        if not QDRANT_AVAILABLE:
            raise ImportError(
                'qdrant-client not installed. '
                'Run: pip install qdrant-client'
            )
        self._client = QdrantClient(url=url)
    

    def _ensure_collection(self, document_id=None):
        existing = [c.name for c in self._client.get_collection().collections]
        if document_id not in existing:
            self._client.create_collection(
                collection_name=document_id,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
    
    def add_chunks(self, document_id, chunks):
        self._ensure_collection(document_id)
        embeddings = embed_documents(chunks)
        points = [
            PointStruct(id=i, vector=emb, payload={'chunk': chunk})
            for i, (emb, chunk) in enumerate(zip(embeddings, chunks))
        ]
        self._client.upsert(collection_name=document_id, points=points)
    
    def search(self, question, document_ids, top_k):
        q_embedding = embed_query(question)
        results = []
        for doc_id in document_ids:
            try:
                hits = self._client.search(
                    collection_name=doc_id,
                    query_vector=q_embedding,
                    limit=top_k
                )
                for hit in hits:
                    results.append({
                        'document_id': doc_id,
                        'chunk': hit.payload['chunk'],
                        'score': 1 - hit.score
                    })
            except Exception:
                continue
        results.sort(key=lambda x: x['score'])
        return results[:top_k]
    
    def list_collections(self):
        return [c.name for c in self._client.get_collections().collections]
    
    def delete_collection(self, document_id):
        self._client.delete_collection(document_id)