import PageWrapper from "../components/PageWrapper";
import { useAuth } from "../context/AuthContext";
import MainButtonLink from "../components/Root/MainButtonLink";
const Root = () => {
  const { jwtToken } = useAuth();
  const isLoggedIn = !!jwtToken;

  return (
    <PageWrapper>
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
        <div className="bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-xl border border-slate-700 p-10 max-w-md w-full text-center">
          <h1 className="text-3xl font-bold text-indigo-400 mb-4">
            Welcome to TaskMaster
          </h1>
          <p className="text-slate-300 mb-6">
            Organize your tasks, track progress, and stay on top of your day.
          </p>

          {isLoggedIn ? (
            <MainButtonLink text="Go to Dashboard" to={"/dashboard"} />
          ) : (
            <MainButtonLink text="Login to Start" to={"/login"} />
          )}
        </div>
      </div>
    </PageWrapper>
  );
};

export default Root;
