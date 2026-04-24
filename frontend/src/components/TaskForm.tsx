import React, { useState, useEffect } from "react";
import type { Tag, Task, TaskFormData } from "../types";

interface Props {
  initial?: Task | null;
  tags: Tag[];
  onSubmit: (data: Partial<TaskFormData>) => Promise<void>;
  onCancel: () => void;
}

const EMPTY: TaskFormData = {
  title: "",
  description: "",
  status: "todo",
  priority: "medium",
  due_date: "",
  tag_ids: [],
  use_ai_priority: false,
};

export function TaskForm({ initial, tags, onSubmit, onCancel }: Props) {
  const [form, setForm] = useState<TaskFormData>(EMPTY);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (initial) {
      setForm({
        title: initial.title,
        description: initial.description ?? "",
        status: initial.status,
        priority: initial.priority,
        due_date: initial.due_date ? initial.due_date.slice(0, 10) : "",
        tag_ids: initial.tags.map((t) => t.id),
        use_ai_priority: false,
      });
    } else {
      setForm(EMPTY);
    }
  }, [initial]);

  const set = (field: keyof TaskFormData, value: unknown) =>
    setForm((f) => ({ ...f, [field]: value }));

  const toggleTag = (id: number) =>
    set(
      "tag_ids",
      form.tag_ids.includes(id) ? form.tag_ids.filter((t) => t !== id) : [...form.tag_ids, id]
    );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.title.trim()) {
      setErrors({ title: "Title is required." });
      return;
    }
    setErrors({});
    setSaving(true);
    try {
      await onSubmit({
        ...form,
        description: form.description || undefined,
        due_date: form.due_date || undefined,
      });
    } catch (err: any) {
      if (err?.body?.errors) {
        const flat: Record<string, string> = {};
        Object.entries(err.body.errors).forEach(([k, v]) => {
          flat[k] = Array.isArray(v) ? v[0] : String(v);
        });
        setErrors(flat);
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      <div>
        <label htmlFor="tf-title">Title *</label>
        <input
          id="tf-title"
          value={form.title}
          onChange={(e) => set("title", e.target.value)}
          placeholder="What needs to be done?"
          aria-required="true"
          aria-describedby={errors.title ? "tf-title-err" : undefined}
        />
        {errors.title && <span id="tf-title-err" style={{ color: "#ef4444", fontSize: 12 }}>{errors.title}</span>}
      </div>

      <div>
        <label htmlFor="tf-desc">Description</label>
        <textarea
          id="tf-desc"
          rows={3}
          value={form.description}
          onChange={(e) => set("description", e.target.value)}
          placeholder="Optional details..."
          style={{ resize: "vertical" }}
        />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div>
          <label htmlFor="tf-status">Status</label>
          <select id="tf-status" value={form.status} onChange={(e) => set("status", e.target.value)}>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </div>
        <div>
          <label htmlFor="tf-priority">Priority</label>
          <select
            id="tf-priority"
            value={form.priority}
            onChange={(e) => set("priority", e.target.value)}
            disabled={form.use_ai_priority}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
        </div>
      </div>

      <div>
        <label htmlFor="tf-due">Due Date</label>
        <input
          id="tf-due"
          type="date"
          value={form.due_date}
          onChange={(e) => set("due_date", e.target.value)}
        />
      </div>

      {tags.length > 0 && (
        <div>
          <label>Tags</label>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 4 }}>
            {tags.map((tag) => (
              <button
                key={tag.id}
                type="button"
                onClick={() => toggleTag(tag.id)}
                style={{
                  background: form.tag_ids.includes(tag.id) ? tag.color : tag.color + "22",
                  color: form.tag_ids.includes(tag.id) ? "#fff" : tag.color,
                  border: `1px solid ${tag.color}`,
                  fontSize: 12,
                  padding: "3px 10px",
                }}
                aria-pressed={form.tag_ids.includes(tag.id)}
              >
                {tag.name}
              </button>
            ))}
          </div>
        </div>
      )}

      <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
        <input
          type="checkbox"
          checked={form.use_ai_priority}
          onChange={(e) => set("use_ai_priority", e.target.checked)}
          style={{ width: "auto" }}
        />
        <span style={{ fontSize: 13 }}>🤖 Use AI to suggest priority</span>
      </label>

      {initial?.ai_priority_reason && !form.use_ai_priority && (
        <p style={{ fontSize: 12, color: "#6366f1", fontStyle: "italic", margin: 0 }}>
          🤖 Previous AI suggestion: {initial.ai_priority_reason}
        </p>
      )}

      <div style={{ display: "flex", gap: 10, justifyContent: "flex-end" }}>
        <button type="button" onClick={onCancel} style={{ background: "#f1f5f9", color: "#475569" }}>
          Cancel
        </button>
        <button type="submit" disabled={saving} style={{ background: "#6366f1", color: "#fff" }}>
          {saving ? "Saving…" : initial ? "Update Task" : "Create Task"}
        </button>
      </div>
    </form>
  );
}
