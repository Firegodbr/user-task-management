import { useState, useEffect, useMemo, useCallback } from "react";
import api from "../../lib/api";
import type { Task, TaskListResponse, TaskResponse, TaskInput } from "../../types/task";
import { motion, AnimatePresence } from "framer-motion";
import TaskForm from "./TaskForm";
import TaskItem from "./TaskItem";
import Pagination from "./Pagination";
import { ITEMS_PER_PAGE } from "./constants";

const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  // Fetch all tasks
  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get<TaskListResponse>("/tasks/");
      if (response.data.success) {
        setTasks(response.data.tasks);
        setError(null);
      } else {
        setError(response.data.error || "Failed to fetch tasks");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Pagination calculations
  const totalPages = useMemo(
    () => Math.ceil(tasks.length / ITEMS_PER_PAGE),
    [tasks.length]
  );

  const paginatedTasks = useMemo(() => {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    return tasks.slice(start, end);
  }, [tasks, currentPage]);

  // Reset to page 1 if current page is out of bounds
  useEffect(() => {
    if (currentPage > totalPages && totalPages > 0) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  // Create task
  const handleCreate = useCallback(
    async (formData: TaskInput) => {
      try {
        const response = await api.post<TaskResponse>("/tasks/", formData);
        if (response.data.success && response.data.task) {
          setTasks((prev) => [...prev, response.data.task!]);
          setIsCreating(false);
          setError(null);
          // Go to last page to see new task
          const newTotalPages = Math.ceil((tasks.length + 1) / ITEMS_PER_PAGE);
          setCurrentPage(newTotalPages);
        } else {
          setError(response.data.error || "Failed to create task");
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to create task");
      }
    },
    [tasks.length]
  );

  // Update task
  const handleUpdate = useCallback(async (id: number, updatedData: TaskInput) => {
    try {
      const response = await api.put<TaskResponse>(`/tasks/${id}`, updatedData);
      if (response.data.success && response.data.task) {
        setTasks((prev) => prev.map((t) => (t.id === id ? response.data.task! : t)));
        setEditingId(null);
        setError(null);
      } else {
        setError(response.data.error || "Failed to update task");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to update task");
    }
  }, []);

  // Delete task
  const handleDelete = useCallback(async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this task?")) return;

    try {
      const response = await api.delete<TaskResponse>(`/tasks/${id}`);
      if (response.data.success) {
        setTasks((prev) => prev.filter((t) => t.id !== id));
        setError(null);
      } else {
        setError(response.data.error || "Failed to delete task");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to delete task");
    }
  }, []);

  const handleEdit = useCallback((id: number) => {
    setEditingId(id);
  }, []);

  const handleCancelEdit = useCallback(() => {
    setEditingId(null);
  }, []);

  const handlePageChange = useCallback((page: number) => {
    setCurrentPage(page);
  }, []);

  const toggleCreating = useCallback(() => {
    setIsCreating((prev) => !prev);
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-indigo-400">My Tasks</h2>
          <p className="text-sm text-slate-400 mt-1">
            {tasks.length} {tasks.length === 1 ? "task" : "tasks"} total
          </p>
        </div>
        <button
          onClick={toggleCreating}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors"
        >
          {isCreating ? "Cancel" : "+ New Task"}
        </button>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-lg"
        >
          {error}
        </motion.div>
      )}

      {isCreating && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          className="bg-slate-700/50 p-4 rounded-lg border border-slate-600"
        >
          <h3 className="text-lg font-semibold text-indigo-400 mb-3">Create New Task</h3>
          <TaskForm onSubmit={handleCreate} />
        </motion.div>
      )}

      <div className="space-y-3">
        {tasks.length === 0 ? (
          <div className="text-center py-12 text-slate-400">
            No tasks yet. Create your first task to get started!
          </div>
        ) : (
          <>
            <AnimatePresence mode="popLayout">
              {paginatedTasks.map((task) => (
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

            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default TaskList;
