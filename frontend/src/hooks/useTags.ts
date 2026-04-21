import { useState, useEffect } from "react";
import { api } from "../api";
import type { Tag } from "../types";

export function useTags() {
  const [tags, setTags] = useState<Tag[]>([]);

  const load = async () => {
    try {
      setTags(await api.tags.list());
    } catch {}
  };

  useEffect(() => { load(); }, []);

  return { tags, reload: load };
}
