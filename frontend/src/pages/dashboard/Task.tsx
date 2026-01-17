import { useParams } from "react-router";
import PageWrapper from "../../components/PageWrapper";
const Task = () => {
  const param = useParams();
  return <PageWrapper>Task: {param.task}</PageWrapper>;
};
export default Task;
