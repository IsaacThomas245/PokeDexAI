import ChatMessages from "@/components/ChatMessages";

function Chatbot({ messages, isLoading, onPromptSelect }) {
  const categories = [
    { label: "Pokémon", prompt: "Who is Charizard?" },
    { label: "Moves", prompt: "What is Earthquake?" },
    { label: "Types", prompt: "What does Dragon resist?" },
    { label: "Abilities", prompt: "What does Intimidate do?" },
    { label: "Evolutions", prompt: "How does Slowpoke evolve?" },
  ];

  return (
    <div className="relative flex flex-col gap-6 pt-6 pb-24">
      {messages.length === 0 && (
        <div className="mt-3 font-urbanist space-y-6">
          <p className="text-primary-blue text-xl font-semibold">
            What do you want to know?
          </p>
          <div className="flex flex-col gap-3">
            {categories.map(({ label, prompt }) => (
              <button
                key={label}
                onClick={() => onPromptSelect(prompt)}
                className="flex justify-between items-center px-4 py-3 rounded-xl border border-primary-blue bg-transparent hover:bg-white/5 transition-colors"
              >
                <span className="text-primary-blue font-semibold text-sm">
                  {label}
                </span>
                <span className="text-gray-500 text-sm">{prompt}</span>
              </button>
            ))}
          </div>
          <p className="text-primary-blue text-xl font-semibold">
            or type your own question below
          </p>
        </div>
      )}

      <ChatMessages messages={messages} isLoading={isLoading} />
    </div>
  );
}

export default Chatbot;
