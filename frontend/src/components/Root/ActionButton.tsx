import type { MouseEventHandler } from "react";

const ActionButton = ({
  clickHandler,
  className,
  text,
}: {
  clickHandler: MouseEventHandler<HTMLButtonElement>;
  className: string;
  text: string;
}) => {
  return (
    <button
      onClick={clickHandler}
      className={
        "px-3 py-1 text-white text-sm rounded transition-colors " + className
      }
    >
      {text}
    </button>
  );
};
export default ActionButton;
