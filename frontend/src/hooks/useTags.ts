import { useState, useEffect } from "react";
import { api } from "../api";
import type { Tag } from "../types";

export function useTags() {
  const [tags, setTags] = useState<Tag[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setError(null);
      setTags(await api.tags.list());
    } catch {
      setError("Failed to load tags.");
    }
  };

  useEffect(() => { load(); }, []);

  return { tags, error, reload: load };
}
