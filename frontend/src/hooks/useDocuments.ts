import { useState, useEffect, useCallback } from "react";
import {
  getDocuments,
  uploadDocument,
  deleteDocument,
  DocumentInfo,
} from "@/lib/api";

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadDocuments = useCallback(async () => {
    const docs = await getDocuments();
    setDocuments(docs);
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const upload = useCallback(async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      await uploadDocument(file);
      await loadDocuments();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }, [loadDocuments]);

  const remove = useCallback(async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      await loadDocuments();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }, [loadDocuments]);

  return { documents, uploading, error, upload, remove, loadDocuments };
}