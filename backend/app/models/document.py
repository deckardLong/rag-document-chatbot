from pydantic import BaseModel

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_indexed: int
    status: int

class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    uploaded_at: str
    chunks: int