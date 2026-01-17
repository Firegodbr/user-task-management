import { useCallback, memo } from "react";
import type { Task, TaskInput } from "../../types/task";
import { motion } from "framer-motion";
import TaskForm from "./TaskForm";

// Memoized Task Item Component
const TaskItem = memo(
  ({
    task,
    isEditing,
    onEdit,
    onDelete,
    onUpdate,
    onCancelEdit,
  }: {
    task: Task;
    isEditing: boolean;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
    onUpdate: (id: number, data: TaskInput) => void;
    onCancelEdit: () => void;
  }) => {
    const handleUpdate = useCallback(
      (data: TaskInput) => {
        onUpdate(task.id, data);
      },
      [task.id, onUpdate],
    );

    const handleEdit = useCallback(() => {
      onEdit(task.id);
    }, [task.id, onEdit]);

    const handleDelete = useCallback(() => {
      onDelete(task.id);
    }, [task.id, onDelete]);

    return (
      <motion.div
        layout
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 20 }}
        className="bg-slate-700/50 p-4 rounded-lg border border-slate-600 hover:border-slate-500 transition-colors"
      >
        {isEditing ? (
          <TaskForm
            onSubmit={handleUpdate}
            onCancel={onCancelEdit}
            initialData={{ desc: task.task, date: task.date }}
          />
        ) : (
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h3 className="text-lg font-medium text-slate-100 mb-1">
                {task.task}
              </h3>
              <p className="text-sm text-slate-400">
                Due: {new Date(task.date).toLocaleDateString()}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleEdit}
                className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        )}
      </motion.div>
    );
  },
);

TaskItem.displayName = "TaskItem";

export default TaskItem;