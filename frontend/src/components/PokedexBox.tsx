import React from "react";

export default function PokedexBox({
  children,
  color = "red",
  className = "",
}) {
  return (
    <div
      className={`pokedex-panel ${color === "blue" ? "blue" : ""} ${className}`}
    >
      <div className="pokedex-header-lights">
        <div className="pokedex-light blue" />
        <div className="pokedex-light yellow" />
        <div className="pokedex-light red" />
      </div>
      {children}
    </div>
  );
}
