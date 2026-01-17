export interface Task {
  id: number;
  task: string;
  date: string;
}

export interface TaskResponse {
  success: boolean;
  task?: Task;
  error?: string;
}

export interface TaskListResponse {
  success: boolean;
  tasks: Task[];
  error?: string;
}

export interface TaskInput {
  desc: string;
  date: string;
}
