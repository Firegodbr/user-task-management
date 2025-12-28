import { Route, Routes, useLocation } from "react-router";
import DashboardLayout from "./layouts/DashboardLayout";
import MainLayout from "./layouts/MainLayout";
import Root from "./pages/Root";
import About from "./pages/About";
import Login from "./pages/sign/Login";
import Register from "./pages/sign/Register";
import Dashboard from "./pages/dashboard/Dashboard";
import Task from "./pages/dashboard/Task";
import TaskCreate from "./pages/dashboard/TaskCreate";
import RequireAuth from "./middleware/RequiredAuth";
import { AnimatePresence } from "framer-motion";
function App() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route element={<MainLayout />}>
          <Route index element={<Root />} />
          <Route path="about" element={<About />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
        </Route>
        <Route element={<RequireAuth />}>
          <Route path="dashboard" element={<DashboardLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="create-task" element={<TaskCreate />} />
            <Route path=":task" element={<Task />} />
          </Route>
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default App;
