import { useState } from "react";
import { useImmer } from "use-immer";
import Chatbot from "@/components/Chatbot";
import ChatInput from "@/components/ChatInput";
import api from "@/api";
import logo from "@/assets/images/logo.svg";

function App() {
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState("");

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage(overrideMessage) {
    const trimmedMessage = (overrideMessage ?? newMessage).trim();
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
        draft[draft.length - 1] = { ...response, loading: false };
      });
    } catch (err) {
      console.error(err);
      setMessages((draft) => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
    }
  }

  function handlePromptSelect(prompt) {
    setNewMessage(prompt);
    submitNewMessage(prompt);
  }

  return (
    <div className="min-h-screen w-full bg-black flex flex-col">
      <header className="sticky top-0 z-50 bg-gradient-to-b from-red-700 via-red-600 to-red-800 border-b border-red-900 shadow-xl rounded-b-3xl">
        <div className="relative w-full px-4 py-3 flex items-center">
          <img src={logo} className="h-10 w-auto" alt="logo" />
          <div className="absolute left-1/2 -translate-x-1/2 text-primary-blue font-bold tracking-widest text-sm">
            POKÉDEX AI
          </div>
          <div className="ml-auto flex items-center gap-3">
            <div className="h-5 w-5 rounded-full bg-red-400 shadow-[0_0_10px_rgba(255,80,80,0.9)] animate-pulse flex items-center justify-center">
              <div className="h-3 w-3 rounded-full bg-red-200"></div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto w-full">
        <div className="max-w-3xl mx-auto px-4">
          <Chatbot
            messages={messages}
            isLoading={isLoading}
            onPromptSelect={handlePromptSelect}
          />
        </div>
      </div>

      <div className="w-full border-t border-primary-blue bg-black sticky bottom-0">
        <div className="max-w-3xl mx-auto px-4">
          <ChatInput
            newMessage={newMessage}
            isLoading={isLoading}
            setNewMessage={setNewMessage}
            submitNewMessage={submitNewMessage}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
