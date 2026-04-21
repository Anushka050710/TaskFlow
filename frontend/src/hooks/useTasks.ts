import { useState, useEffect, useRef } from "react";
import { api } from "../api";
import type { PaginatedTasks, TaskFilters } from "../types";

export function useTasks(filters: TaskFilters) {
  const [data, setData] = useState<PaginatedTasks | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const filtersRef = useRef(filters);
  filtersRef.current = filters;

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.tasks.list(filtersRef.current).then((result) => {
      if (!cancelled) setData(result);
    }).catch(() => {
      if (!cancelled) setError("Failed to load tasks.");
    }).finally(() => {
      if (!cancelled) setLoading(false);
    });
    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(filters), tick]);

  const reload = () => setTick((t) => t + 1);

  return { data, loading, error, reload };
}
