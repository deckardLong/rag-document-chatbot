import { useRef } from "react";
import { DocumentInfo } from "@/lib/api";

interface Props {
  documents: DocumentInfo[];
  uploading: boolean;
  onUpload: (file: File) => void;
  onDelete: (documentId: string) => void;
  error: string | null;
}

export function DocumentUpload({
  documents,
  uploading,
  onUpload,
  onDelete,
  error,
}: Props) {
  const fileRef = useRef<HTMLInputElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
      e.target.value = "";
    }
  };

  return (
    <div className="flex flex-col gap-3 h-full">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">
          Documents
        </h2>
        <span className="text-xs text-gray-500">{documents.length} files</span>
      </div>

      <button
        onClick={() => fileRef.current?.click()}
        disabled={uploading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50
          text-white text-sm py-2 px-3 rounded-lg transition-colors font-medium"
      >
        {uploading ? "Uploading..." : "+ Upload File"}
      </button>

      <input
        ref={fileRef}
        type="file"
        accept=".pdf,.docx,.txt"
        className="hidden"
        onChange={handleChange}
      />

      {error && (
        <p className="text-xs text-red-400 bg-red-900/20 px-3 py-2 rounded-lg">
          {error}
        </p>
      )}

      <div className="flex flex-col gap-2 overflow-y-auto flex-1">
        {documents.length === 0 && (
          <p className="text-xs text-gray-600 text-center mt-4">
            No documents yet.
            <br />
            Upload a PDF, DOCX, or TXT file.
          </p>
        )}
        {documents.map((doc) => (
          <div
            key={doc.document_id}
            className="bg-gray-800 rounded-lg p-3 text-xs group relative"
          >
            <p className="font-medium text-gray-200 truncate pr-5">
              {doc.filename}
            </p>
            <p className="text-gray-500 mt-0.5">{doc.chunks} chunks</p>
            <button
              onClick={() => onDelete(doc.document_id)}
              className="absolute top-2 right-2 text-gray-600 hover:text-red-400
                opacity-0 group-hover:opacity-100 transition-opacity"
              title="Delete"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}