import { useState, KeyboardEvent } from "react";

interface Props {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: Props) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim() || disabled) return;
    onSend(input.trim());
    setInput("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4 border-t border-gray-800 flex gap-3 items-end">
      <textarea
        className="flex-1 bg-gray-800 rounded-xl px-4 py-3 text-sm outline-none
          focus:ring-2 focus:ring-blue-500 resize-none min-h-[48px] max-h-[160px]
          text-gray-100 placeholder-gray-500"
        placeholder="Ask a question about your documents... (Enter to send, Shift+Enter for newline)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
        disabled={disabled}
      />
      <button
        onClick={handleSend}
        disabled={disabled || !input.trim()}
        className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed
          px-5 py-3 rounded-xl text-sm font-medium text-white transition-colors"
      >
        {disabled ? "..." : "Send"}
      </button>
    </div>
  );
}