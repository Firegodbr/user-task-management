import { memo } from "react";
import type { Task, TaskInput } from "../../types/task";
import { motion } from "framer-motion";
import TaskForm from "./TaskForm";
import DeleteButton from "../Root/DeleteButton";
import EditButton from "../Root/EditButton";
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
    const handleUpdate = (data: TaskInput) => {
      onUpdate(task.id, data);
    };
    const handleEdit = () => {
      onEdit(task.id);
    };

    const handleDelete = () => {
      onDelete(task.id);
    };

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
              <EditButton handleEdit={handleEdit} />
              <DeleteButton handleDelete={handleDelete} />
            </div>
          </div>
        )}
      </motion.div>
    );
  },
);

TaskItem.displayName = "TaskItem";

export default TaskItem;
