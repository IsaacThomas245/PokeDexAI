import warningIcon from "@/assets/images/warning.svg";

export default function MessageUnknown({ content }) {
  return (
    <div className="flex items-start gap-2 text-sm text-gray-300 mt-2">
      <img
        src={warningIcon}
        alt="info"
        className="h-5 w-5 opacity-80 select-none"
      />
      <span className="leading-snug">
        {"Try asking about a Pokémon, move, type, ability, or evolution."}
      </span>
    </div>
  );
}
