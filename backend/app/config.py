from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    LLM_MODEL: str = 'gemini-1.5-flash'
    EMBEDDING_MODEL: str = 'all-MiniLM-L6-V2'

    VECTOR_DB: str = 'chroma'
    CHROMA_PERSIST_DIR: str = './data/chroma_db'

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5

    UPLOAD_DIR: str = './data/uploads'
    MAX_UPLOAD_SIZE_MB: int = 20

    class Config:
        env_file = '.env'

settings = Settings()