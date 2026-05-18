import uuid, os, json
from datetime import datetime, UTC
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.indexer import index_document
from app.vector_store.chroma import list_collections, delete_collection
from app.config import settings

router = APIRouter()

META_FILE = './data/document_meta.json'

def _load_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE) as f:
            return json.load(f)
    return {}

def _save_meta(meta):
    os.makedirs(os.path.dirname(META_FILE), exist_ok=True)
    with open(META_FILE, 'w') as f:
        json.dump(meta, f)

@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    allowed = {'.pdf', '.docx', '.txt'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(400, f'File type {ext} not supported.')
    
    document_id = str(uuid.uuid4())
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f'{document_id}{ext}')

    with open(file_path, 'wb') as f:
        f.write(await file.read())
    
    chunks_count = index_document(file_path, document_id)

    meta = _load_meta()
    meta[document_id] = {
        'filename': file.filename,
        'uploaded_at': datetime.now(UTC).isoformat(),
        'chunks': chunks_count,
    }
    _save_meta(meta)

    return {
        'document_id': document_id,
        'filename': file.filename,
        'chunks_indexed': chunks_count,
        'status': 'success'
    }

@router.delete('/documents/{document_id}')
async def delete_document(document_id):
    delete_collection(document_id)
    meta = _load_meta()
    meta.pop(document_id, None)
    _save_meta(meta)
    return {'status': 'deleted'}