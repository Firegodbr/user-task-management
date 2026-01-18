import { useCallback, useState, memo } from "react";
import type { Task, TaskInput, TaskResponse } from "../../types/task";
import TaskItem from "./TaskItem";
import { AnimatePresence } from "motion/react";
import Pagination from "./Pagination";
import api from "../../lib/api";

interface TaskTableProps {
  tasks: Task[];
  setTasks: React.Dispatch<React.SetStateAction<Task[]>>;
  setError: React.Dispatch<React.SetStateAction<string | null>>;
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  fetchTasks: (page: number) => Promise<void>;
}
const TaskTable = memo(({
  tasks,
  setTasks,
  setError,
  currentPage,
  totalPages,
  onPageChange,
  fetchTasks
}: TaskTableProps) => {
  const [editingId, setEditingId] = useState<number | null>(null);
  const handleUpdate = useCallback(
    async (id: number, updatedData: TaskInput) => {
      try {
        const response = await api.put<TaskResponse>(
          `/tasks/${id}`,
          updatedData,
        );
        if (response.data.success && response.data.task) {
          setTasks((prev) =>
            prev.map((t) => (t.id === id ? response.data.task! : t)),
          );
          setEditingId(null);
          setError(null);
        } else {
          setError(response.data.error || "Failed to update task");
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to update task");
      }
    },
    [],
  );

  // Delete task
  const handleDelete = useCallback(async (id: number) => {
    try {
      const response = await api.delete<TaskResponse>(`/tasks/${id}`);
      if (response.data.success) {
        setError(null);
        // Refresh current page after deletion
        await fetchTasks(currentPage);
      } else {
        setError(response.data.error || "Failed to delete task");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to delete task");
    }
  }, [currentPage, fetchTasks]);

  const handleEdit = (id: number) => {
    setEditingId(id);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
  };

  return (
    <div className="space-y-3">
      {tasks.length === 0 ? (
        <div className="text-center py-12 text-slate-400">
          No tasks yet. Create your first task to get started!
        </div>
      ) : (
        <>
          <AnimatePresence mode="popLayout">
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                isEditing={editingId === task.id}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onUpdate={handleUpdate}
                onCancelEdit={handleCancelEdit}
              />
            ))}
          </AnimatePresence>

          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={onPageChange}
            />
          )}
        </>
      )}
    </div>
  );
});
export default TaskTable;
