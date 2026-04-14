export default function MessageMove({ data }) {
  if (!data) return null;

  const { name, power, accuracy, type, category, effect } = data;

  return (
    <div className="markdown-container mt-2 text-sm space-y-2">
      <div>
        <strong>Name:</strong> {name}
      </div>
      <div className="flex gap-2 mt-1">
        <strong>Type:</strong>
        <img key={type} src={`/type_sprites/${type}.png`} alt={type} />
      </div>
      <div>
        <div className="flex gap-2 mt-1">
          <strong>Category:</strong>
          <img
            key={category}
            src={`/move_sprites/move-${category}.png`}
            alt={category}
          />
        </div>
      </div>
      <div>
        <strong>Power:</strong> {power ?? "—"}
      </div>
      <div>
        <strong>Accuracy:</strong> {accuracy ?? "—"}
      </div>
      <div>
        <strong>Effect:</strong> {effect}
      </div>
    </div>
  );
}
