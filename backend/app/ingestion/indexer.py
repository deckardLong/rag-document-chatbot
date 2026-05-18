from app.ingestion.loader import load_document
from app.ingestion.chunker import split_text
from app.vector_store.chroma import add_chunks

def index_document(file_path, document_id):
    text = load_document(file_path)
    chunks = split_text(text)
    add_chunks(document_id, chunks)
    return len(chunks)