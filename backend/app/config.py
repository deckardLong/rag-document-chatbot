from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(extra="ignore") 

    GOOGLE_API_KEY: str
    LLM_MODEL: str = "gemini-2.5-flash"
    EMBED_MODEL: str = "models/gemini-embedding-001"

    VECTOR_DB: str = "chroma"
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5

    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE_MB: int = 20

settings = Settings()