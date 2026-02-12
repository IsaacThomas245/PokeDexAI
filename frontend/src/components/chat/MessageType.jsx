export default function MessageType({ data }) {
  if (!data) return null;

  // Pokemon combined matchup (4x, 2x, 1/2x, 1/4x, immune)
  const isCombined =
    data.quadruple_weak_to ||
    data.double_weak_to ||
    data.half_resistant_to ||
    data.quarter_resistant_to ||
    data.immune_to;

  if (isCombined) {
    return (
      <div className="markdown-container mt-2 text-sm space-y-2">
        {data.quadruple_weak_to?.length > 0 && (
          <div>
            <strong>4x Weak to:</strong>
            <ul className="list-disc ml-5">
              {data.quadruple_weak_to.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </div>
        )}

        {data.double_weak_to?.length > 0 && (
          <div>
            <strong>2x Weak to:</strong>
            <ul className="list-disc ml-5">
              {data.double_weak_to.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </div>
        )}

        {data.half_resistant_to?.length > 0 && (
          <div>
            <strong>½× Resistant to:</strong>
            <ul className="list-disc ml-5">
              {data.half_resistant_to.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </div>
        )}

        {data.quarter_resistant_to?.length > 0 && (
          <div>
            <strong>¼× Resistant to:</strong>
            <ul className="list-disc ml-5">
              {data.quarter_resistant_to.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </div>
        )}

        {data.immune_to?.length > 0 && (
          <div>
            <strong>Immune to:</strong>
            <ul className="list-disc ml-5">
              {data.immune_to.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  // Type → Type matchups (double_damage_from, half_damage_from, etc.)
  return (
    <div className="markdown-container mt-2 text-sm space-y-2">
      {data.double_damage_from?.length > 0 && (
        <div>
          <strong>Weak to:</strong>
          <ul className="list-disc ml-5">
            {data.double_damage_from.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </div>
      )}

      {data.half_damage_from?.length > 0 && (
        <div>
          <strong>Resistant to:</strong>
          <ul className="list-disc ml-5">
            {data.half_damage_from.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </div>
      )}

      {data.no_damage_from?.length > 0 && (
        <div>
          <strong>Immune to:</strong>
          <ul className="list-disc ml-5">
            {data.no_damage_from.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
