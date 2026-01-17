import type { MouseEventHandler } from "react";
import ActionButton from "./ActionButton";
const EditButton = ({
  handleEdit,
}: {
  handleEdit: MouseEventHandler<HTMLButtonElement>;
}) => {
  return (
    <ActionButton
      clickHandler={handleEdit}
      text="Edit"
      className="bg-blue-600 hover:bg-blue-700"
    />
  );
};
export default EditButton;
