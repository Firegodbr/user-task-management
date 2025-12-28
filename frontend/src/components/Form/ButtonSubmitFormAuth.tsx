const ButtonSubmitFormAuth = ({ text }: { text: string }) => (
  <button
    type="submit"
    className=" bg-indigo-500 hover:bg-indigo-600 focus:bg-indigo-700 text-white font-semibold py-3 rounded-lg transition-colors duration-200 mt-4"
  >
    {text}
  </button>
);
export default ButtonSubmitFormAuth