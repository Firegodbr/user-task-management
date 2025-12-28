import PageWrapper from "../../components/PageWrapper";
import { Link } from "react-router";
import { useFormState } from "react-dom";
import TextInputFormAuth from "../../components/Form/TextInputFormAuth";
import ButtonSubmitFormAuth from "../../components/Form/ButtonSubmitFormAuth";
interface FormState {
  username: string;
  password: string;
}

const Login = () => {
  const handleSubmit = async (
    _previousState: FormState | undefined,
    formData: FormData
  ): Promise<FormState> => {
    const username = String(formData.get("username") ?? "");
    const password = String(formData.get("password") ?? "");
    return { username, password };
  };

  const [_formState, formAction] = useFormState(handleSubmit, {
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
              formAction(data);
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
