import { Link } from "react-router";

const MainButton = ({ text, to }: { text: string; to: string }) => (
  <Link
    to={to}
    className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-lg transition-all duration-200 cursor-pointer"
  >
    {text}
  </Link>
);
export default MainButton;
