import PageWrapper from "../../components/PageWrapper";
import { Link } from "react-router";
import { toast } from "react-toastify";
import TextInputFormAuth from "../../components/Form/TextInputFormAuth";
import ButtonSubmitFormAuth from "../../components/Form/ButtonSubmitFormAuth";
import api from "../../lib/api";
import { useCallback, useActionState, startTransition } from "react";
import { validateRegistration } from "../../lib/validation";
type FormState = {
  username: string;
  password: string;
  password2: string;
};

const Register = () => {
  const handleSubmit = useCallback(
    async (
      _previousState: FormState | null,
      formData: FormData
    ): Promise<null> => {
      const username = String(formData.get("username") ?? "");
      const password = String(formData.get("password") ?? "");
      const password2 = String(formData.get("password2") ?? "");
      if (!(await validateRegistration(username, password, password2)))
        return null;
      const formDataSend = new FormData();
      formDataSend.append("username", username);
      formDataSend.append("password", password);

      try {
        const response = await api.post("/auth/register", formDataSend, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        if (response.status === 200) {
          toast.success("Registration successful");
        }
      } catch (e: unknown) {
        if (e instanceof Error) console.error(e.message);
      }
      return null;
    },
    []
  );

  const [_formState, formAction] = useActionState(handleSubmit, {
    username: "",
    password: "",
    password2: "",
  });
  return (
    <PageWrapper>
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
        <div className="bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-xl border border-slate-700 p-10 max-w-md w-full text-center">
          <h1 className="text-3xl font-bold text-indigo-400 mb-6">Register</h1>
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
            <TextInputFormAuth
              name="password2"
              placeholder="Confirm Password"
              type="password"
              required
            />
            <ButtonSubmitFormAuth text="Register" />
          </form>
          <p className="text-slate-400 mt-4 text-sm">
            Already have an account?{" "}
            <Link to="/login" className="text-indigo-400 hover:underline">
              Login
            </Link>
          </p>
        </div>
      </div>
    </PageWrapper>
  );
};

export default Register;
