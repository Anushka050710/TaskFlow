import type { PaginatedTasks, Tag, Task, TaskFilters, TaskFormData } from "./types";

// In production set REACT_APP_API_BASE to your backend URL e.g. https://taskflow-api.onrender.com/api
const BASE = process.env.REACT_APP_API_BASE ?? "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body);
  }
  if (res.status === 204) return undefined as unknown as T;
  return res.json();
}

export class ApiError extends Error {
  constructor(public status: number, public body: unknown) {
    super(`API error ${status}`);
  }
}

export const api = {
  tasks: {
    list: (filters: TaskFilters = {}): Promise<PaginatedTasks> => {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([k, v]) => {
        if (v !== undefined && v !== "") params.set(k, String(v));
      });
      const qs = params.toString();
      return request(`/tasks/${qs ? `?${qs}` : ""}`);
    },
    get: (id: number): Promise<Task> => request(`/tasks/${id}`),
    create: (data: Partial<TaskFormData>): Promise<Task> =>
      request("/tasks/", { method: "POST", body: JSON.stringify(data) }),
    update: (id: number, data: Partial<TaskFormData>): Promise<Task> =>
      request(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
    delete: (id: number): Promise<void> =>
      request(`/tasks/${id}`, { method: "DELETE" }),
  },
  tags: {
    list: (): Promise<Tag[]> => request("/tags/"),
    create: (name: string, color: string): Promise<Tag> =>
      request("/tags/", { method: "POST", body: JSON.stringify({ name, color }) }),
    delete: (id: number): Promise<void> =>
      request(`/tags/${id}`, { method: "DELETE" }),
  },
};
