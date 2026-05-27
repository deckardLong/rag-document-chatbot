import { Source } from "@/lib/api";

interface Props {
  sources: Source[];
}

export function SourceList({ sources }: Props) {
  if (sources.length === 0) return null;

  return (
    <div className="px-6 pb-3">
      <p className="text-xs text-gray-500 mb-2 font-medium uppercase tracking-wide">
        Sources
      </p>
      <div className="flex flex-col gap-2">
        {sources.map((s, i) => (
          <div
            key={i}
            className="bg-gray-800/60 border border-gray-700 rounded-lg px-3 py-2 text-xs"
          >
            <p className="text-blue-400 font-medium mb-1">
              📎 {s.filename || s.document_id}
            </p>
            <p className="text-gray-400 line-clamp-2">{s.chunk}</p>
          </div>
        ))}
      </div>
    </div>
  );
}