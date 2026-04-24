export type TaskStatus = "todo" | "in_progress" | "done";
export type Priority = "low" | "medium" | "high" | "critical";

export interface Tag {
  id: number;
  name: string;
  color: string;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: Priority;
  ai_priority_reason: string | null;
  due_date: string | null;
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

export interface PaginatedTasks {
  items: Task[];
  total: number;
  page: number;
  pages: number;
  per_page: number;
}

export interface TaskFilters {
  status?: TaskStatus | "";
  priority?: Priority | "";
  tag_id?: number | "";
  search?: string;
  page?: number;
}

export interface TaskFormData {
  title: string;
  description: string;
  status: TaskStatus;
  priority: Priority;
  due_date: string;
  tag_ids: number[];
  use_ai_priority: boolean;
}
