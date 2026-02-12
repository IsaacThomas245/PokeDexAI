import errorIcon from "@/assets/images/error.svg";

export default function MessageError({ content }) {
  return (
    <div
      className={`flex items-center gap-1 text-sm text-error-red ${
        content ? "mt-2" : ""
      }`}
    >
      <img className="h-5 w-5" src={errorIcon} alt="error" />
      <span>Error generating the response</span>
    </div>
  );
}
