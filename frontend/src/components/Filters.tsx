import React from "react";
import type { Tag, TaskFilters } from "../types";

interface Props {
  filters: TaskFilters;
  tags: Tag[];
  onChange: (f: TaskFilters) => void;
}

export function Filters({ filters, tags, onChange }: Props) {
  const set = (key: keyof TaskFilters, value: string | number) =>
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
      {tags.length > 0 && (
        <select
          value={filters.tag_id ?? ""}
          onChange={(e) => set("tag_id", e.target.value ? Number(e.target.value) : "")}
          style={{ width: "auto" }}
          aria-label="Filter by tag"
        >
          <option value="">All tags</option>
          {tags.map((tag) => (
            <option key={tag.id} value={tag.id}>
              {tag.name}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}
