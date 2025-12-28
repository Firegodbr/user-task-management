import PageWrapper from "../components/PageWrapper";

const About = () => {
  return (
    <PageWrapper>
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
        <div className="bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-xl border border-slate-700 p-10 max-w-2xl w-full text-center">
          <h1 className="text-3xl font-bold text-indigo-400 mb-4">
            About TaskMaster
          </h1>
          <p className="text-slate-300 mb-6">
            TaskMaster is a modern task management app designed to help you stay
            organized and productive. Track your tasks, manage deadlines, and
            achieve your goals efficiently.
          </p>
          <p className="text-slate-400">
            Built with React, Tailwind CSS, and Framer Motion, it offers a smooth
            and interactive experience, making task management simple and
            enjoyable.
          </p>
        </div>
      </div>
    </PageWrapper>
  );
};

export default About;
