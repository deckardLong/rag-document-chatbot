# 🤖 RAG Document Chatbot

An intelligent Q&A chatbot powered by your own documents, built on the **RAG (Retrieval-Augmented Generation)** architecture — combining semantic search with a large language model (LLM) to deliver accurate answers grounded in your document content.

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the App](#-running-the-app)
- [How It Works](#-how-it-works)
- [API Reference](#-api-reference)
- [Tech Stack](#-tech-stack)

---

## 🏗 Architecture Overview

```
┌─────────────┐      Upload documents       ┌──────────────────┐
│   Frontend  │ ──────────────────────────▶ │   Backend (API)  │
│  (Next.js)  │ ◀────────────────────────── │   (FastAPI)      │
│             │      Questions / Answers     │                  │
└─────────────┘                             └────────┬─────────┘
                                                     │
                    ┌────────────────────────────────┤
                    │                                │
            ┌───────▼──────┐            ┌────────────▼──────┐
            │  Vector DB   │            │     LLM API        │
            │  (ChromaDB / │            │  (OpenAI / Gemini  │
            │   Qdrant)    │            │   / Claude)        │
            └──────────────┘            └───────────────────┘
```

**RAG Pipeline:**

1. **Indexing** — Documents are split into chunks → embeddings are generated → stored in a vector database
2. **Retrieval** — The user's question is embedded → most relevant chunks are retrieved
3. **Generation** — Retrieved chunks + question are passed to the LLM to produce an answer

---

## 📁 Project Structure

```
rag-document-chatbot/
│
├── backend/                        # API server (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entrypoint
│   │   ├── config.py               # Configuration (env vars, constants)
│   │   │
│   │   ├── api/                    # Route definitions
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # POST /chat — receive question, return answer
│   │   │   └── documents.py        # POST /upload, GET /documents
│   │   │
│   │   ├── core/                   # Core RAG logic
│   │   │   ├── __init__.py
│   │   │   ├── embedder.py         # Generate embeddings from text
│   │   │   ├── retriever.py        # Vector search, return relevant chunks
│   │   │   ├── generator.py        # Call LLM to generate answers
│   │   │   └── pipeline.py         # Connect Retriever + Generator
│   │   │
│   │   ├── ingestion/              # Document processing & ingestion
│   │   │   ├── __init__.py
│   │   │   ├── loader.py           # Read PDF, DOCX, TXT, ...
│   │   │   ├── chunker.py          # Split text into chunks
│   │   │   └── indexer.py          # Embed chunks and store in vector DB
│   │   │
│   │   ├── vector_store/           # Vector database integration
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Abstract VectorStore class
│   │   │   ├── chroma.py           # Adapter for ChromaDB
│   │   │   └── qdrant.py           # Adapter for Qdrant (optional)
│   │   │
│   │   └── models/                 # Pydantic schemas
│   │       ├── __init__.py
│   │       ├── chat.py             # ChatRequest, ChatResponse
│   │       └── document.py         # DocumentInfo, UploadResponse
│   │
│   ├── data/
│   │   ├── uploads/                # User-uploaded documents
│   │   └── chroma_db/              # Locally persisted vector DB data
│   │
│   ├── tests/
│   │   ├── test_ingestion.py
│   │   ├── test_retriever.py
│   │   └── test_pipeline.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                       # User interface (Next.js)
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx            # Main chat page
│   │   │   └── globals.css
│   │   │
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx      # Display conversation history
│   │   │   ├── MessageBubble.tsx   # Message bubble component
│   │   │   ├── ChatInput.tsx       # Question input field
│   │   │   ├── DocumentUpload.tsx  # Document upload UI
│   │   │   └── SourceList.tsx      # Display citation sources
│   │   │
│   │   ├── hooks/
│   │   │   ├── useChat.ts          # Chat API call logic
│   │   │   └── useDocuments.ts     # Document upload/management logic
│   │   │
│   │   └── lib/
│   │       └── api.ts              # HTTP client for backend calls
│   │
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml              # Run the full stack
├── docker-compose.dev.yml          # Dev environment stack
├── .gitignore
└── README.md                       # This file
```

---

## 💻 System Requirements

| Tool    | Minimum Version          |
|---------|--------------------------|
| Python  | 3.10+                    |
| Node.js | 18+                      |
| Docker  | 20+                      |
| RAM     | 4 GB (8 GB recommended)  |

---

## ⚙️ Installation

### Option 1: Run with Docker (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/rag-document-chatbot.git
cd rag-document-chatbot

# 2. Create the environment file
cp backend/.env.example backend/.env
# → Edit backend/.env and fill in your API keys (see Configuration below)

# 3. Build and start
docker-compose up --build
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

---

### Option 2: Run manually (development)

**Backend:**

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create the .env file
cp .env.example .env
# → Fill in your API keys in .env

# Start the server
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

---

## 🔧 Configuration

Create `backend/.env` based on `.env.example`:

```env
# ── LLM Provider ──────────────────────────────────────
# Choose one of the providers below:

# OpenAI
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini

# Or Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=claude-3-haiku-20240307

# Or Google Gemini
GOOGLE_API_KEY=AIza...
LLM_MODEL=gemini-1.5-flash

# ── Embedding Model ───────────────────────────────────
EMBEDDING_MODEL=text-embedding-3-small   # OpenAI embedding
# EMBEDDING_MODEL=all-MiniLM-L6-v2       # Run locally (no API key needed)

# ── Vector Database ───────────────────────────────────
VECTOR_DB=chroma                         # chroma | qdrant
CHROMA_PERSIST_DIR=./data/chroma_db

# ── Chunking ──────────────────────────────────────────
CHUNK_SIZE=500                           # Tokens per chunk
CHUNK_OVERLAP=50                         # Token overlap between chunks

# ── Retrieval ─────────────────────────────────────────
TOP_K=5                                  # Number of chunks to retrieve per query

# ── Upload ────────────────────────────────────────────
UPLOAD_DIR=./data/uploads
MAX_UPLOAD_SIZE_MB=20
```

---

## 🚀 Running the App

### Basic workflow

```
1. Open http://localhost:3000
2. Upload a document (PDF, DOCX, TXT)  ← automatically indexed
3. Type your question in the chat box
4. Receive an answer with cited sources
```

### Index documents via CLI

```bash
# Index a single file
python backend/app/ingestion/indexer.py --file ./data/my_document.pdf

# Index an entire directory
python backend/app/ingestion/indexer.py --dir ./data/uploads/
```

### Run tests

```bash
cd backend
pytest tests/ -v
```

---

## 🔄 How It Works

### Upload & Indexing

```
User uploads file
      │
      ▼
loader.py          — reads the file and extracts plain text
      │
      ▼
chunker.py         — splits text into smaller chunks
      │
      ▼
embedder.py        — converts each chunk into a numeric vector
      │
      ▼
VectorStore        — saves vectors + metadata to ChromaDB
```

### Chat & Retrieval

```
User types a question
      │
      ▼
embedder.py        — embeds the question into a vector
      │
      ▼
retriever.py       — finds the TOP_K most similar chunks in the DB
      │
      ▼
generator.py       — combines chunks + question into a prompt, calls the LLM
      │
      ▼
Returns answer + list of cited sources
```

---

## 📡 API Reference

### `POST /upload`
Upload and index a new document.

```json
// Request: multipart/form-data
{ "file": "<binary>" }

// Response
{
  "document_id": "abc123",
  "filename": "report.pdf",
  "chunks_indexed": 42,
  "status": "success"
}
```

### `POST /chat`
Send a question and receive an answer grounded in the documents.

```json
// Request
{
  "question": "What is the return policy?",
  "document_ids": ["abc123"],   // optional — omit to search across all documents
  "chat_history": []            // optional — include to maintain conversation context
}

// Response
{
  "answer": "According to the document, the return policy states...",
  "sources": [
    {
      "document_id": "abc123",
      "filename": "report.pdf",
      "page": 3,
      "chunk": "...excerpt content..."
    }
  ]
}
```

### `GET /documents`
Retrieve the list of uploaded documents.

```json
// Response
[
  {
    "document_id": "abc123",
    "filename": "report.pdf",
    "uploaded_at": "2025-05-12T10:00:00Z",
    "chunks": 42
  }
]
```

### `DELETE /documents/{document_id}`
Delete a document and all its associated vectors.

---

## 🛠 Tech Stack

| Component         | Technology                                           |
|------------------|------------------------------------------------------|
| Backend framework | FastAPI                                             |
| LLM              | OpenAI GPT / Anthropic Claude / Google Gemini        |
| Embedding        | OpenAI `text-embedding-3-small` / HuggingFace local  |
| Vector database  | ChromaDB (default) / Qdrant                          |
| Document parsing | PyMuPDF, python-docx, LangChain loaders              |
| Frontend         | Next.js 14 + TypeScript + Tailwind CSS               |
| Container        | Docker + Docker Compose                              |

---

## 🗺 Roadmap

- [ ] Multi-turn conversation support (maintain context across turns)
- [ ] Reranking with cross-encoders to improve retrieval accuracy
- [ ] Support for Excel, PowerPoint, and web URL ingestion
- [ ] User authentication and document-level access control
- [ ] Streaming responses (token-by-token output)
- [ ] RAG quality evaluation (RAGAS metrics)

---

## 🐛 Troubleshooting

**Error: `No module named 'chromadb'`**
```bash
pip install chromadb --upgrade
```

**Error: `API key not found`**
→ Check that your `.env` file contains the correct key and that the server has been restarted.

**Upload succeeds but the chatbot can't find the content**
→ Review `CHUNK_SIZE` and `TOP_K` in `.env`. Try increasing `TOP_K` to 10.

**Frontend cannot connect to the backend**
→ Make sure `NEXT_PUBLIC_API_URL=http://localhost:8000` is set in `frontend/.env.local`.

---

## 📄 License

MIT License — see the [LICENSE](./LICENSE) file for details.