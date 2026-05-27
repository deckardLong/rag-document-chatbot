from google import genai
from app.config import settings

_client = genai.Client(
    api_key=settings.GOOGLE_API_KEY,
    http_options={"api_version": "v1"}
)

def generate_answer(question, context_chunks, chat_history):
    context = '\n\n---\n\n'.join(context_chunks)

    prompt = f"""You are a helpful assistant. Answer the user's question using ONLY the context provided below. 
    If the answer is not in the context, say "I couldn't find relevant information in the documents."

    Context:
    {context}

    Question: {question}
    Answer:"""

    response = _client.models.generate_content(
        model=settings.LLM_MODEL,
        contents=prompt,
    )
    return response.text