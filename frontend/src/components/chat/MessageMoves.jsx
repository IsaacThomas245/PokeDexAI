import React from "react";

export default function MessageMoves({ moves }) {
  if (!moves || moves.length === 0) return null;

  const pretty = (method) =>
    method.replace("-", " ").replace(/\b\w/g, (c) => c.toUpperCase());

  const levelUpMoves = moves
    .filter((m) => m.method === "level-up")
    .sort((a, b) => a.level - b.level);

  const machineMoves = moves.filter((m) => m.method === "machine");
  const eggMoves = moves.filter((m) => m.method === "egg");
  const tutorMoves = moves.filter((m) => m.method === "tutor");

  const otherMoves = moves.filter(
    (m) => !["level-up", "machine", "egg", "tutor"].includes(m.method),
  );

  const renderGroup = (title, list, formatter) => {
    if (!list || list.length === 0) return null;

    return (
      <div className="mb-3">
        <div className="font-semibold mb-1">{title}</div>
        <ul className="space-y-1">
          {list.map((m, idx) => (
            <li key={idx} className="flex justify-between text-sm">
              <span className="font-medium">{m.name}</span>
              <span className="text-primary-blue">{formatter(m)}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div>
      <strong>Moves:</strong>

      <div className="max-h-64 overflow-y-auto mt-2 border border-primary-blue rounded p-3 bg-black/30 space-y-4 text-white">
        {renderGroup("Level-Up Moves", levelUpMoves, (m) => `Lv ${m.level}`)}
        {renderGroup("TM / Machine Moves", machineMoves, () => "TM")}
        {renderGroup("Egg Moves", eggMoves, () => "Egg")}
        {renderGroup("Tutor Moves", tutorMoves, () => "Tutor")}
        {renderGroup("Other Moves", otherMoves, (m) => pretty(m.method))}
      </div>
    </div>
  );
}
