import React, { useState, useCallback } from "react";
import { api } from "./api";
import { useTasks } from "./hooks/useTasks";
import { useTags } from "./hooks/useTags";
import { TaskCard } from "./components/TaskCard";
import { TaskForm } from "./components/TaskForm";
import { Modal } from "./components/Modal";
import { Filters } from "./components/Filters";
import type { Task, TaskFilters, TaskFormData } from "./types";

export default function App() {
  const [filters, setFilters] = useState<TaskFilters>({ page: 1 });
  const { data, loading, error, reload } = useTasks(filters);
  const { tags, reload: reloadTags } = useTags();

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Task | null>(null);

  const openCreate = () => { setEditing(null); setModalOpen(true); };
  const openEdit = (task: Task) => { setEditing(task); setModalOpen(true); };
  const closeModal = () => setModalOpen(false);

  const handleSubmit = useCallback(async (formData: Partial<TaskFormData>) => {
    if (editing) {
      await api.tasks.update(editing.id, formData);
    } else {
      await api.tasks.create(formData);
    }
    closeModal();
    reload();
  }, [editing, reload]);

  const handleDelete = useCallback(async (id: number) => {
    if (!window.confirm("Delete this task?")) return;
    await api.tasks.delete(id);
    reload();
  }, [reload]);

  return (
    <div style={{ maxWidth: 860, margin: "0 auto", padding: "32px 16px" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 28 }}>
        <div>
          <h1 style={{ fontSize: 26, fontWeight: 800, color: "#1e293b" }}>TaskFlow</h1>
          <p style={{ fontSize: 13, color: "#94a3b8", marginTop: 2 }}>AI-powered task management</p>
        </div>
        <button onClick={openCreate} style={{ background: "#6366f1", color: "#fff", padding: "10px 20px", fontSize: 14 }}>
          + New Task
        </button>
      </div>

      {/* Filters */}
      <div style={{ marginBottom: 20 }}>
        <Filters filters={filters} onChange={setFilters} />
      </div>

      {/* Task list */}
      {loading && <p style={{ color: "#94a3b8", textAlign: "center", padding: 40 }}>Loading…</p>}
      {error && <p style={{ color: "#ef4444", textAlign: "center", padding: 40 }}>{error}</p>}

      {!loading && data && (
        <>
          <p style={{ fontSize: 13, color: "#94a3b8", marginBottom: 12 }}>
            {data.total} task{data.total !== 1 ? "s" : ""}
          </p>
          {data.items.length === 0 ? (
            <div style={{ textAlign: "center", padding: 60, color: "#94a3b8" }}>
              <p style={{ fontSize: 32, marginBottom: 8 }}>📋</p>
              <p>No tasks yet. Create one to get started.</p>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {data.items.map((task) => (
                <TaskCard key={task.id} task={task} onEdit={openEdit} onDelete={handleDelete} />
              ))}
            </div>
          )}

          {/* Pagination */}
          {data.pages > 1 && (
            <div style={{ display: "flex", gap: 8, justifyContent: "center", marginTop: 24 }}>
              {Array.from({ length: data.pages }, (_, i) => i + 1).map((p) => (
                <button
                  key={p}
                  onClick={() => setFilters((f) => ({ ...f, page: p }))}
                  style={{
                    background: p === data.page ? "#6366f1" : "#f1f5f9",
                    color: p === data.page ? "#fff" : "#475569",
                    padding: "6px 12px",
                  }}
                  aria-current={p === data.page ? "page" : undefined}
                >
                  {p}
                </button>
              ))}
            </div>
          )}
        </>
      )}

      {/* Modal */}
      {modalOpen && (
        <Modal title={editing ? "Edit Task" : "New Task"} onClose={closeModal}>
          <TaskForm
            initial={editing}
            tags={tags}
            onSubmit={handleSubmit}
            onCancel={closeModal}
          />
        </Modal>
      )}
    </div>
  );
}
