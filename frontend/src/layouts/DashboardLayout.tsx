import { Outlet } from "react-router";

const DashboardLayout = () => {
  return (
    <>
      <header>
        <nav>
          <a href="/">Home</a> | <a href="/about">About</a>
        </nav>
      </header>

      <main>
        <Outlet />
      </main>

      <footer>
        <p>© 2025 My App</p>
      </footer>
    </>
  );
};

export default DashboardLayout;
