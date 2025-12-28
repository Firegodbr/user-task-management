import { useParams } from "react-router";
const Task = () => {
  const param = useParams();
  return <div>Task: {param.task}</div>;
};
export default Task;
