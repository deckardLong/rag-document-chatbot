from google import genai
from google.genai import types
from app.config import settings

_client = genai.Client(
    api_key=settings.GOOGLE_API_KEY,
    http_options={"api_version": "v1"}
)

def embed_documents(texts):
    result = _client.models.embed_content(
        model=settings.EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return [e.values for e in result.embeddings]

def embed_query(text):
    result = _client.models.embed_content(
        model=settings.EMBED_MODEL,
        contents=[text],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return result.embeddings[0].values