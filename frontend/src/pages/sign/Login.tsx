import PageWrapper from "../../components/PageWrapper";
import { Link } from "react-router";
import { useActionState, startTransition, useCallback } from "react";
import TextInputFormAuth from "../../components/Form/TextInputFormAuth";
import ButtonSubmitFormAuth from "../../components/Form/ButtonSubmitFormAuth";
import api from "../../lib/api";
import { useAuth } from "../../context/AuthContext";
interface FormState {
  username: string;
  password: string;
}

const Login = () => {
  const { login } = useAuth();
  const handleSubmit = useCallback(
    async (
      _previousState: FormState | undefined,
      formData: FormData
    ): Promise<FormState> => {
      const username = String(formData.get("username") ?? "");
      const password = String(formData.get("password") ?? "");

      try {
        const response = await api.post("/auth/token", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        if (response.status === 200) {
          const { access_token } = response.data;
          login(access_token);
        }
      } catch (error: unknown) {
        if (error instanceof Error) console.log(error.message);
      }
      return { username, password };
    },
    []
  );

  const [_formState, formAction] = useActionState(handleSubmit, {
    username: "",
    password: "",
  });

  return (
    <PageWrapper>
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
        <div className="bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-xl border border-slate-700 p-10 max-w-md w-full text-center">
          <h1 className="text-3xl font-bold text-indigo-400 mb-6">Login</h1>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const data = new FormData(e.currentTarget);
              startTransition(() => formAction(data));
            }}
            className="flex flex-col gap-4"
          >
            <TextInputFormAuth
              name="username"
              placeholder="Username"
              required
            />
            <TextInputFormAuth
              name="password"
              placeholder="Password"
              type="password"
              required
            />
            <ButtonSubmitFormAuth text="Login" />
          </form>

          <p className="text-slate-400 mt-4 text-sm">
            Don't have an account yet?{" "}
            <Link to="/register" className="text-indigo-400 hover:underline">
              Register
            </Link>
          </p>
        </div>
      </div>
    </PageWrapper>
  );
};

export default Login;
