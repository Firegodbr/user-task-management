import { Route, Routes, useLocation } from "react-router";
import MainLayout from "./layouts/MainLayout";
import Root from "./pages/Root";
import About from "./pages/About";
import Login from "./pages/sign/Login";
import Register from "./pages/sign/Register";
import Dashboard from "./pages/dashboard/Dashboard";
import { AnimatePresence } from "framer-motion";
import RequireAuth from "./middleware/RequiredAuth";
import RequireAdmin from "./middleware/RequiredAdmin";
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
          <Route element={<RequireAuth />}>
            <Route path="dashboard">
              <Route index element={<Dashboard />} />
            </Route>
            <Route path="admin" element={<RequireAdmin />}></Route>
          </Route>
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default App;
