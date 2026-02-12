export default function MessageMove({ data }) {
  if (!data) return null;

  const { name, power, accuracy, type, category, effect } = data;

  return (
    <div className="markdown-container mt-2 text-sm space-y-2">
      <div>
        <strong>Name:</strong> {name}
      </div>
      <div>
        <strong>Type:</strong> {type}
      </div>
      <div>
        <strong>Category:</strong> {category}
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
