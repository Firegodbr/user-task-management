import type { MouseEventHandler } from "react";
import ActionButton from "./ActionButton";
const DeleteButton = ({
  handleDelete,
}: {
  handleDelete: MouseEventHandler<HTMLButtonElement>;
}) => {
  return (
    <ActionButton
      clickHandler={handleDelete}
      text="Edit"
      className="bg-red-600 hover:bg-red-700"
    />
  );
};
export default DeleteButton;
