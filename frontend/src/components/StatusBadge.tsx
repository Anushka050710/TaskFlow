import React from "react";
import type { TaskStatus } from "../types";

const LABELS: Record<TaskStatus, string> = {
  todo: "To Do",
  in_progress: "In Progress",
  done: "Done",
};

const COLORS: Record<TaskStatus, string> = {
  todo: "#94a3b8",
  in_progress: "#6366f1",
  done: "#22c55e",
};

export function StatusBadge({ status }: { status: TaskStatus }) {
  return (
    <span
      style={{
        background: COLORS[status],
        color: "#fff",
        borderRadius: 4,
        padding: "2px 8px",
        fontSize: 12,
        fontWeight: 500,
      }}
    >
      {LABELS[status]}
    </span>
  );
}
