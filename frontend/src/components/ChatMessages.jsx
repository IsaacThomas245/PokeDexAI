import Markdown from "react-markdown";
import useAutoScroll from "@/hooks/useAutoScroll";
import Spinner from "@/components/Spinner";
import userIcon from "@/assets/images/user.svg";
import MessagePokemon from "./chat/MessagePokemon";
import MessageMove from "./chat/MessageMove";
import MessageAbility from "./chat/MessageAbility";
import MessageType from "./chat/MessageType";
import MessageEvolution from "./chat/MessageEvolution";
import MessageText from "./chat/MessageText";
import MessageError from "./chat/MessageError";

function ChatMessages({ messages, isLoading }) {
  const scrollContentRef = useAutoScroll(isLoading);

  return (
    <div ref={scrollContentRef} className="grow space-y-4">
      {messages.map(
        ({ role, content, type, data, loading, error: hasError }, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-4 py-4 px-3 rounded-xl ${role === "user" ? "bg-primary-blue/10" : ""}`}
          >
            {role === "user" && (
              <img
                className="h-[26px] w-[26px] shrink-0"
                src={userIcon}
                alt="user"
              />
            )}
            <div>
              <div className="markdown-container">
                {loading && !content ? (
                  <Spinner />
                ) : role === "assistant" ? (
                  <>
                    <Markdown>{content}</Markdown>

                    {type === "pokemon" && <MessagePokemon data={data} />}
                    {type === "move" && <MessageMove data={data} />}
                    {type === "ability" && <MessageAbility data={data} />}
                    {type === "type" && <MessageType data={data} />}
                    {type === "evolution" && <MessageEvolution data={data} />}
                    {type === "text" && <MessageText data={data} />}
                    {type === "error" && <MessageError />}
                  </>
                ) : (
                  <div className="whitespace-pre-line">{content}</div>
                )}
              </div>

              {hasError && <MessageError content={content} />}
            </div>
          </div>
        ),
      )}
    </div>
  );
}

export default ChatMessages;
