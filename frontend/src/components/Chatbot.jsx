import ChatMessages from "@/components/ChatMessages";

function Chatbot({ messages, isLoading }) {
  return (
    <div className="relative flex flex-col gap-6 pt-6 pb-24">
      {messages.length === 0 && (
        <div className="mt-3 font-urbanist text-primary-blue text-xl font-light space-y-2">
          <p>Welcome to your Pokédex Assistant!</p>

          <p>
            I'm your AI-powered guide to the world of Pokémon. Ask me about
            moves, types, abilities, evolutions, or any Pokémon you're curious
            about, and I'll break it down with clear, game-accurate info.
          </p>

          <p>
            Whether you're building a competitive team or just exploring the
            Pokédex, I'm here to help you understand how everything fits
            together.
          </p>
        </div>
      )}

      <ChatMessages messages={messages} isLoading={isLoading} />
    </div>
  );
}

export default Chatbot;
