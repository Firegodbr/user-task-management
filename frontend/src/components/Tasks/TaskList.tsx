import { useState, useEffect, useCallback } from "react";
import api from "../../lib/api";
import type {
  Task,
  TaskListResponse,
  TaskResponse,
  TaskInput,
} from "../../types/task";
import { motion } from "framer-motion";
import TaskForm from "./TaskForm";
import TaskTable from "./TaskTable";

const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalTasks, setTotalTasks] = useState(0);
  const pageSize = 10;

  // Fetch paginated tasks
  const fetchTasks = useCallback(async (page: number = 1) => {
    try {
      setLoading(true);
      const response = await api.get<TaskListResponse>("/tasks/", {
        params: { page, page_size: pageSize },
      });
      if (response.data.success) {
        setTasks(response.data.tasks);
        setTotalPages(response.data.total_pages);
        setTotalTasks(response.data.total);
        setCurrentPage(response.data.page);
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
    fetchTasks(currentPage);
  }, [fetchTasks, currentPage]);

  const handleCreate = useCallback(
    async (formData: TaskInput) => {
      try {
        const response = await api.post<TaskResponse>("/tasks/", formData);
        if (response.data.success && response.data.task) {
          setIsCreating(false);
          setError(null);
          // Refresh current page to show new task
          await fetchTasks(currentPage);
        } else {
          setError(response.data.error || "Failed to create task");
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to create task");
      }
    },
    [currentPage, fetchTasks],
  );

  const toggleCreating = () => {
    setIsCreating((prev) => !prev);
  };

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
            {totalTasks} {totalTasks === 1 ? "task" : "tasks"} total
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
          <h3 className="text-lg font-semibold text-indigo-400 mb-3">
            Create New Task
          </h3>
          <TaskForm onSubmit={handleCreate} />
        </motion.div>
      )}

      <TaskTable
        tasks={tasks}
        setTasks={setTasks}
        setError={setError}
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
        fetchTasks={fetchTasks}
      />
    </div>
  );
};

export default TaskList;
