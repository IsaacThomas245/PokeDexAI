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
import PokedexBox from "./PokedexBox";

function ChatMessages({ messages, isLoading }) {
  const scrollContentRef = useAutoScroll(isLoading);

  return (
    <div ref={scrollContentRef} className="grow space-y-4">
      {messages.map(
        ({ role, content, type, data, loading, error: hasError }, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-4 w-full ${
              role === "user"
                ? "py-4 px-3 rounded-xl bg-primary-blue/15 shadow-[0_0_8px_rgba(28,199,199,0.3)]"
                : ""
            }`}
          >
            {role === "user" && (
              <img
                className="h-[26px] w-[26px] shrink-0"
                src={userIcon}
                alt="user"
              />
            )}

            <div className="flex-1">
              <div className="markdown-container w-full">
                {loading && !content ? (
                  <Spinner />
                ) : role === "assistant" ? (
                  <>
                    {(content || data) && (
                      <PokedexBox className="w-full" color="primary-blue">
                        <Markdown>{content}</Markdown>

                        {type === "pokemon" && <MessagePokemon data={data} />}
                        {type === "move" && <MessageMove data={data} />}
                        {type === "ability" && <MessageAbility data={data} />}
                        {type === "type" && <MessageType data={data} />}
                        {type === "evolution" && (
                          <MessageEvolution data={data} />
                        )}
                        {type === "text" && <MessageText data={data} />}
                        {type === "error" && <MessageError />}
                      </PokedexBox>
                    )}
                  </>
                ) : (
                  <div className="whitespace-pre-line text-primary-blue/90">
                    {content}
                  </div>
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
