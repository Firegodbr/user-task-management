import { Outlet } from "react-router";
import { NavLink, Link } from "react-router";
import { motion } from "framer-motion";
import { useAuth } from "../context/AuthContext";

const basePages = [
  { url: "/", page: "Home" },
  { url: "/about", page: "About" },
];

const DashboardLayout = () => {
  const { jwtToken, logout } = useAuth();

  // Check localStorage directly to avoid flash during auth check
  const hasStoredAuth = !!localStorage.getItem("jwt_payload");

  const pages =
    jwtToken || hasStoredAuth
      ? [...basePages, { url: "/dashboard", page: "Dashboard" }]
      : basePages;
  return (
    <div className="min-h-screen flex flex-col bg-linear-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur bg-slate-900/70 border-b border-slate-700">
        <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
          <h1 className="text-xl font-bold tracking-wide text-indigo-400">
            <Link to="/">My App</Link>
          </h1>

          <div className="flex gap-6 text-sm font-medium relative">
            {pages.map((page, i) => (
              <NavLink
                key={`${page.url}-${i}`}
                to={page.url}
                className={({ isActive }) =>
                  `relative px-1 pb-1 transition-colors ${
                    isActive
                      ? "text-indigo-400"
                      : "text-slate-300 hover:text-indigo-300"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {page.page}

                    {isActive && (
                      <motion.span
                        layoutId="nav-underline"
                        className="absolute left-0 right-0 -bottom-1 h-0.5 bg-indigo-400 rounded-full"
                        transition={{
                          type: "spring",
                          stiffness: 500,
                          damping: 30,
                        }}
                      />
                    )}
                  </>
                )}
              </NavLink>
            ))}
            <div
              className="relative px-1 pb-1 transition-colors text-slate-300 hover:text-indigo-300 cursor-pointer"
              onClick={logout}
            >
              Logout
            </div>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4">
        <div className="w-full bg-slate-800/80 backdrop-blur rounded-2xl shadow-xl border border-slate-700 p-8">
          <Outlet />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700 text-center py-4 text-xs text-slate-400">
        © 2025 My App. All rights reserved.
      </footer>
    </div>
  );
};

export default DashboardLayout;
