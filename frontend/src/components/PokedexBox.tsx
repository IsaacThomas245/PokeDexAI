import React from "react";

export default function PokedexBox({
  children,
  color = "red",
  className = "",
}) {
  const colorClass =
    color === "primary-blue"
      ? "primary-blue"
      : color === "blue"
        ? "blue"
        : "red";

  return (
    <div className={`pokedex-panel ${colorClass} ${className}`}>
      <div className="pokedex-header-lights">
        <div className="pokedex-light blue" />
        <div className="pokedex-light yellow" />
        <div className="pokedex-light red" />
      </div>
      {children}
    </div>
  );
}
