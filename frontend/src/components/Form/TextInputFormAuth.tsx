type TextInputFormAuthProps = {
  name: string;
  type?: string;
  placeholder: string;
  required?: boolean;
};

const TextInputFormAuth = ({ name, type = "text", placeholder, required = false }: TextInputFormAuthProps) => (
  <input
    type={type}
    name={name}
    placeholder={placeholder}
    required={required}
    className="px-4 py-2 rounded-lg border border-slate-600 bg-slate-900 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
  />
);

export default TextInputFormAuth