import React from "react";
import type { TaskFilters } from "../types";

interface Props {
  filters: TaskFilters;
  onChange: (f: TaskFilters) => void;
}

export function Filters({ filters, onChange }: Props) {
  const set = (key: keyof TaskFilters, value: string) =>
    onChange({ ...filters, [key]: value, page: 1 });

  return (
    <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
      <input
        placeholder="Search tasks…"
        value={filters.search ?? ""}
        onChange={(e) => set("search", e.target.value)}
        style={{ maxWidth: 220 }}
        aria-label="Search tasks"
      />
      <select
        value={filters.status ?? ""}
        onChange={(e) => set("status", e.target.value)}
        style={{ width: "auto" }}
        aria-label="Filter by status"
      >
        <option value="">All statuses</option>
        <option value="todo">To Do</option>
        <option value="in_progress">In Progress</option>
        <option value="done">Done</option>
      </select>
      <select
        value={filters.priority ?? ""}
        onChange={(e) => set("priority", e.target.value)}
        style={{ width: "auto" }}
        aria-label="Filter by priority"
      >
        <option value="">All priorities</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
        <option value="critical">Critical</option>
      </select>
    </div>
  );
}
