import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)
_model = genai.GenerativeModel(settings.LLM_MODEL)

def generate_answer(question, context_chunks, chat_history):
    context = '\n\n---\n\n'.join(context_chunks)

    prompt = f"""You are a helpful assistant. Answer the user's question using ONLY the context provided below. 
    If the answer is not in the context, say "I couldn't find relevant information in the documents."

    Context:
    {context}

    Question: {question}
    Answer:"""

    response = _model.generate_content(prompt)
    return response.text