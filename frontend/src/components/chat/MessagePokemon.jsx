import React from "react";
import MessageMoves from "./MessageMoves";

export default function MessagePokemon({ data }) {
  if (!data) return null;

  const { types, stats, abilities, moves } = data;

  return (
    <div className="markdown-container mt-2 space-y-3 text-sm">
      <div>
        <strong>Types:</strong>
        <ul className="list-disc ml-5">
          {types.map((t) => (
            <li key={t}>{t}</li>
          ))}
        </ul>
      </div>

      <div>
        <strong>Base Stats:</strong>
        <ul className="list-disc ml-5">
          {Object.entries(stats).map(([stat, value]) => (
            <li key={stat}>
              {stat}: {value}
            </li>
          ))}
        </ul>
      </div>

      <div>
        <strong>Abilities:</strong>
        <ul className="list-disc ml-5">
          {abilities.map((a) => (
            <li key={a}>{a}</li>
          ))}
        </ul>
      </div>

      <MessageMoves moves={moves} />
    </div>
  );
}
