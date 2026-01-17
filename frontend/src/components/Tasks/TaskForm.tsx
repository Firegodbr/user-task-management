import type { TaskInput } from "../../types/task";
import { useState, useCallback } from "react";

const TaskForm = ({
  onSubmit,
  onCancel,
  initialData,
}: {
  onSubmit: (data: TaskInput) => void;
  onCancel?: () => void;
  initialData?: TaskInput;
}) => {
  const [formData, setFormData] = useState<TaskInput>(
    initialData || {
      desc: "",
      date: new Date().toISOString().split("T")[0],
    },
  );

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (!formData.desc.trim()) return;
      onSubmit(formData);
    },
    [formData, onSubmit],
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div>
        <label className="block text-sm text-slate-300 mb-1">
          Task Description
        </label>
        <input
          type="text"
          value={formData.desc}
          onChange={(e) => setFormData({ ...formData, desc: e.target.value })}
          placeholder="Enter task description..."
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
          required
        />
      </div>
      <div>
        <label className="block text-sm text-slate-300 mb-1">Due Date</label>
        <input
          type="date"
          value={formData.date}
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:border-indigo-500"
          required
        />
      </div>
      <div className="flex gap-2">
        <button
          type="submit"
          className="flex-1 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors"
        >
          {initialData ? "Save" : "Create Task"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 px-4 py-2 bg-slate-600 hover:bg-slate-700 text-white rounded-lg transition-colors"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default TaskForm;
