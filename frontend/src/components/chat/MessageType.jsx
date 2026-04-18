export default function MessageType({ data }) {
  if (!data) return null;

  console.log("MessageType received:", data);

  // offense
  const isOffense =
    data.super_effective || data.not_very_effective || data.no_effect;

  if (isOffense) {
    return (
      <div className="markdown-container mt-2 text-sm space-y-2">
        {data.super_effective?.length > 0 && (
          <div>
            <strong>Super effective against:</strong>
            <ul className="list-disc ml-5">
              {data.super_effective.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}

        {data.not_very_effective?.length > 0 && (
          <div>
            <strong>Not very effective against:</strong>
            <ul className="list-disc ml-5">
              {data.not_very_effective.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}

        {data.no_effect?.length > 0 && (
          <div>
            <strong>No effect on:</strong>
            <ul className="list-disc ml-5">
              {data.no_effect.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  // dual type defense
  const isCombinedDefense =
    data.quadruple_weak_to ||
    data.double_weak_to ||
    data.half_resistant_to ||
    data.quarter_resistant_to ||
    data.immune_to;

  if (isCombinedDefense) {
    return (
      <div className="markdown-container mt-2 text-sm space-y-2">
        {data.quadruple_weak_to?.length > 0 && (
          <div>
            <strong>4× Weak to:</strong>
            <ul className="list-disc ml-5">
              {data.quadruple_weak_to.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}

        {data.double_weak_to?.length > 0 && (
          <div>
            <strong>2× Weak to:</strong>
            <ul className="list-disc ml-5">
              {data.double_weak_to.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}

        {data.half_resistant_to?.length > 0 && (
          <div>
            <strong>½× Resistant to:</strong>
            <ul className="list-disc ml-5">
              {data.half_resistant_to.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}

        {data.quarter_resistant_to?.length > 0 && (
          <div>
            <strong>¼× Resistant to:</strong>
            <ul className="list-disc ml-5">
              {data.quarter_resistant_to.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}

        {data.immune_to?.length > 0 && (
          <div>
            <strong>Immune to:</strong>
            <ul className="list-disc ml-5">
              {data.immune_to.map((t) => (
                <img
                  key={t}
                  src={`/type_sprites/${t}.png`}
                  alt={t}
                  className="h-8 w-14"
                />
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  // single type defense
  return (
    <div className="markdown-container mt-2 text-sm space-y-2">
      {data.double_damage_from?.length > 0 && (
        <div>
          <strong>Weak to:</strong>
          <ul className="list-disc ml-5">
            {data.double_damage_from.map((t) => (
              <img
                key={t}
                src={`/type_sprites/${t}.png`}
                alt={t}
                className="h-8 w-14"
              />
            ))}
          </ul>
        </div>
      )}

      {data.half_damage_from?.length > 0 && (
        <div>
          <strong>Resistant to:</strong>
          <ul className="list-disc ml-5">
            {data.half_damage_from.map((t) => (
              <img
                key={t}
                src={`/type_sprites/${t}.png`}
                alt={t}
                className="h-8 w-14"
              />
            ))}
          </ul>
        </div>
      )}

      {data.no_damage_from?.length > 0 && (
        <div>
          <strong>Immune to:</strong>
          <ul className="list-disc ml-5">
            {data.no_damage_from.map((t) => (
              <img
                key={t}
                src={`/type_sprites/${t}.png`}
                alt={t}
                className="h-8 w-14"
              />
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
