"use client";
import { useState, useRef, useEffect } from "react";
import { sendMessage, uploadDocument, getDocuments, ChatMessage, Source } from "@/lib/api";

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const [docs, setDocs] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => { loadDocs(); }, []);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  async function loadDocs() {
    const data = await getDocuments();
    setDocs(data);
  }

  async function handleSend() {
    if (!input.trim() || loading) return;
    const userMsg: ChatMessage = { role: "user", content: input };
    const newHistory = [...messages, userMsg];
    setMessages(newHistory);
    setInput("");
    setLoading(true);
    try {
      const res = await sendMessage(input, messages);
      setMessages([...newHistory, { role: "assistant", content: res.answer }]);
      setSources(res.sources);
    } catch {
      setMessages([...newHistory, { role: "assistant", content: "Error: could not get response." }]);
    }
    setLoading(false);
  }

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    await uploadDocument(file);
    await loadDocs();
    setUploading(false);
    e.target.value = "";
  }

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 border-r border-gray-800 p-4 flex flex-col gap-4">
        <h2 className="text-lg font-bold">📄 Documents</h2>
        <button
          onClick={() => fileRef.current?.click()}
          className="bg-blue-600 hover:bg-blue-700 text-white text-sm py-2 px-3 rounded-lg"
        >
          {uploading ? "Uploading..." : "+ Upload File"}
        </button>
        <input ref={fileRef} type="file" accept=".pdf,.docx,.txt" className="hidden" onChange={handleUpload} />
        <div className="flex flex-col gap-2 overflow-y-auto">
          {docs.map((d) => (
            <div key={d.document_id} className="bg-gray-800 rounded-lg p-2 text-xs">
              <p className="font-medium truncate">{d.filename}</p>
              <p className="text-gray-400">{d.chunks} chunks</p>
            </div>
          ))}
        </div>
      </div>

      {/* Chat area */}
      <div className="flex flex-col flex-1">
        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-20">
              <p className="text-2xl">🤖</p>
              <p className="mt-2">Upload a document and ask me anything about it.</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-2xl px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap
                ${m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-800 text-gray-100"}`}>
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 px-4 py-3 rounded-2xl text-sm text-gray-400">Thinking...</div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Sources */}
        {sources.length > 0 && (
          <div className="px-6 pb-2">
            <p className="text-xs text-gray-500 mb-1">Sources:</p>
            <div className="flex gap-2 flex-wrap">
              {sources.slice(0, 3).map((s, i) => (
                <div key={i} className="bg-gray-800 text-xs text-gray-300 px-3 py-1 rounded-full truncate max-w-xs">
                  📎 {s.filename}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="p-4 border-t border-gray-800 flex gap-3">
          <input
            className="flex-1 bg-gray-800 rounded-xl px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask a question about your documents..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-5 py-3 rounded-xl text-sm font-medium"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}