import React from "react";
import type { Task } from "../types";
import { PriorityBadge } from "./PriorityBadge";
import { StatusBadge } from "./StatusBadge";

interface Props {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

export function TaskCard({ task, onEdit, onDelete }: Props) {
  const due = task.due_date ? new Date(task.due_date) : null;
  const isOverdue = due && due < new Date() && task.status !== "done";

  return (
    <div
      style={{
        background: "#fff",
        border: "1px solid #e2e8f0",
        borderRadius: 10,
        padding: "16px 18px",
        display: "flex",
        flexDirection: "column",
        gap: 8,
        boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 8 }}>
        <span style={{ fontWeight: 600, fontSize: 15, flex: 1 }}>{task.title}</span>
        <div style={{ display: "flex", gap: 6, flexShrink: 0 }}>
          <PriorityBadge priority={task.priority} />
          <StatusBadge status={task.status} />
        </div>
      </div>

      {task.description && (
        <p style={{ fontSize: 13, color: "#64748b", lineHeight: 1.5 }}>{task.description}</p>
      )}

      {task.ai_priority_reason && (
        <p style={{ fontSize: 12, color: "#6366f1", fontStyle: "italic" }}>
          🤖 {task.ai_priority_reason}
        </p>
      )}

      <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
        {task.tags.map((tag) => (
          <span
            key={tag.id}
            style={{
              background: tag.color + "22",
              color: tag.color,
              border: `1px solid ${tag.color}55`,
              borderRadius: 4,
              padding: "1px 8px",
              fontSize: 12,
              fontWeight: 500,
            }}
          >
            {tag.name}
          </span>
        ))}
      </div>

      {due && (
        <p style={{ fontSize: 12, color: isOverdue ? "#ef4444" : "#94a3b8" }}>
          {isOverdue ? "⚠ Overdue: " : "Due: "}
          {due.toLocaleDateString()}
        </p>
      )}

      <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
        <button
          onClick={() => onEdit(task)}
          style={{ background: "#6366f1", color: "#fff", fontSize: 13 }}
          aria-label={`Edit task ${task.title}`}
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          style={{ background: "#fee2e2", color: "#ef4444", fontSize: 13 }}
          aria-label={`Delete task ${task.title}`}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
