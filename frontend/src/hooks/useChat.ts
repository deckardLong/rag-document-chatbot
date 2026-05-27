import { useState, useCallback } from "react";
import { sendMessage, ChatMessage, Source } from "@/lib/api";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendQuestion = useCallback(async (question: string) => {
    if (!question.trim() || loading) return;

    const userMessage: ChatMessage = { role: "user", content: question };
    const updatedHistory = [...messages, userMessage];
    setMessages(updatedHistory);
    setLoading(true);
    setError(null);
    setSources([]);

    try {
      const res = await sendMessage(question, messages);
      setMessages([
        ...updatedHistory,
        { role: "assistant", content: res.answer },
      ]);
      setSources(res.sources);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setMessages([
        ...updatedHistory,
        { role: "assistant", content: "Sorry, I couldn't get a response." },
      ]);
    } finally {
      setLoading(false);
    }
  }, [messages, loading]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setSources([]);
    setError(null);
  }, []);

  return { messages, sources, loading, error, sendQuestion, clearChat };
}