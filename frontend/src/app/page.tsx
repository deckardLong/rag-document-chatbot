"use client";
import { useChat } from "@/hooks/useChat";
import { useDocuments } from "@/hooks/useDocuments";
import { ChatWindow } from "@/components/ChatWindow";
import { ChatInput } from "@/components/ChatInput";
import { DocumentUpload } from "@/components/DocumentUpload";
import { SourceList } from "@/components/SourceList";

export default function Home() {
  const { messages, sources, loading, sendQuestion, clearChat } = useChat();
  const { documents, uploading, error, upload, remove } = useDocuments();

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 border-r border-gray-800 p-4 flex flex-col">
        <div className="mb-4">
          <h1 className="text-base font-bold text-white">📄 RAG Chatbot</h1>
          <p className="text-xs text-gray-500 mt-0.5">Powered by Gemini</p>
        </div>

        <div className="flex-1 min-h-0">
          <DocumentUpload
            documents={documents}
            uploading={uploading}
            onUpload={upload}
            onDelete={remove}
            error={error}
          />
        </div>

        <button
          onClick={clearChat}
          className="mt-4 w-full text-xs text-gray-500 hover:text-gray-300
            py-2 border border-gray-800 hover:border-gray-600 rounded-lg transition-colors"
        >
          Clear chat
        </button>
      </div>

      {/* Main chat area */}
      <div className="flex flex-col flex-1 min-w-0">
        <ChatWindow messages={messages} loading={loading} />
        <SourceList sources={sources} />
        <ChatInput onSend={sendQuestion} disabled={loading} />
      </div>
    </div>
  );
}