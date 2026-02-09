import { useState } from "react";
import { useImmer } from "use-immer";
import api from "@/api";
import ChatMessages from "@/components/ChatMessages";
import ChatInput from "@/components/ChatInput";

function Chatbot() {
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState("");

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages((draft) => [
      ...draft,
      { role: "user", content: trimmedMessage },
      { role: "assistant", loading: true },
    ]);
    setNewMessage("");

    try {
      const response = await api.sendChatMessage(trimmedMessage);

      setMessages((draft) => {
        draft[draft.length - 1] = {
          ...response,
          loading: false,
        };
      });
    } catch (err) {
      console.error(err);
      setMessages((draft) => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
    }
  }

  return (
    <div className="relative grow flex flex-col gap-6 pt-6">
      {messages.length === 0 && (
        <div className="mt-3 font-urbanist text-primary-blue text-xl font-light space-y-2">
          <p>👋 Welcome to your Pokédex Assistant!</p>

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
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;
