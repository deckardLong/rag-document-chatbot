const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Source {
    document_id: string;
    filename: string;
    chunk: string;
}

export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

export interface ChatResponse {
    answer: string;
    sources: Source[];
}

export async function sendMessage(
  question: string,
  history: ChatMessage[]
): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, chat_history: history }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  return res.json();
}

export async function uploadDocument(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/upload`, { method: "POST", body: form });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function getDocuments() {
  try {
    const res = await fetch(`${API_URL}/documents`);
    if (!res.ok) return [];
    const data = await res.json();
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}