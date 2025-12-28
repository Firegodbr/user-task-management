import { Navigate, Outlet } from "react-router";
import { useAuth } from "../context/AuthContext";

const RequireAuth = () => {
  const { token } = useAuth();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default RequireAuth;
