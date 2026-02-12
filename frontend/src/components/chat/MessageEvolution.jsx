import React from "react";

export default function MessageEvolution({ data }) {
  if (!data || !data.species) return null;

  const renderNode = (node) => {
    return (
      <li>
        {node.species.name}

        {node.details && (
          <div className="ml-4 text-xs text-gray-500">
            {node.details?.text && (
              <div className="ml-4 text-xs text-gray-500">
                {node.details.text}
              </div>
            )}
          </div>
        )}

        {node.regional_forms && (
          <ul className="ml-5 list-disc">
            {node.regional_forms.map((rf, idx) => (
              <li key={idx}>{rf.species.name} (regional form)</li>
            ))}
          </ul>
        )}

        {node.evolves_to && node.evolves_to.length > 0 && (
          <ul className="ml-5 list-disc">
            {node.evolves_to.map((child, idx) => (
              <React.Fragment key={idx}>{renderNode(child)}</React.Fragment>
            ))}
          </ul>
        )}
      </li>
    );
  };

  return (
    <div className="markdown-container mt-2 text-sm">
      <strong>Evolution Chain:</strong>
      <ul className="list-disc ml-5">{renderNode(data)}</ul>
    </div>
  );
}
