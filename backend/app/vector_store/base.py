from abc import ABC, abstractmethod

class BaseVectorStore(ABC):
    @abstractmethod
    def add_chunks(self, document_id, chunks):
        return None
    
    @abstractmethod
    def search(self, question, document_ids, top_k):
        return []
    
    @abstractmethod
    def list_collections(self):
        return []
    
    @abstractmethod
    def delete_collection(self, document_id):
        return None