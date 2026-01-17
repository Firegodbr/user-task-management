import { Navigate, Outlet } from "react-router";
import { useAuth } from "../context/AuthContext";

const RequireAdmin = () => {
  const { jwtToken } = useAuth();
  if (jwtToken?.role !== "admin") return <Navigate to={"/dashboard"} replace />;
  return <Outlet />;
};
export default RequireAdmin;
