export default function MessageAbility({ data }) {
  if (!data) return null;

  // Single ability lookup
  const isSingleAbility =
    typeof data === "object" &&
    !Array.isArray(data) &&
    data.name &&
    data.effect;

  if (isSingleAbility) {
    return (
      <div className="markdown-container mt-2 text-sm space-y-2">
        <div>
          <strong>Effect:</strong> {data.effect}
        </div>
      </div>
    );
  }

  // Pokemon ability list
  return (
    <div className="markdown-container mt-2 text-sm space-y-3">
      {data.map((ability) => (
        <div key={ability.name}>
          {}
          <strong>{ability.name}:</strong>
          <div className="ml-4">{ability.effect}</div>
        </div>
      ))}
    </div>
  );
}
