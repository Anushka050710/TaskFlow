import React from "react";
import type { Priority } from "../types";

const COLORS: Record<Priority, string> = {
  low: "#22c55e",
  medium: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};

interface Props {
  priority: Priority;
}

export function PriorityBadge({ priority }: Props) {
  return (
    <span
      style={{
        background: COLORS[priority],
        color: "#fff",
        borderRadius: 4,
        padding: "2px 8px",
        fontSize: 12,
        fontWeight: 600,
        textTransform: "uppercase",
        letterSpacing: "0.05em",
      }}
    >
      {priority}
    </span>
  );
}
