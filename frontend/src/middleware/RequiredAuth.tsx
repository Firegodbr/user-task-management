import { Navigate, Outlet } from "react-router";
import { useAuth } from "../context/AuthContext";

const RequireAuth = () => {
  const { isAuthenticated, isLoading } = useAuth();

  // Wait for authentication check to complete
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-slate-300">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default RequireAuth;
