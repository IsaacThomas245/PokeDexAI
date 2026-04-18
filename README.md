# Pokedex AI

**Live Site:** [https://pokedexai.me](https://pokedexai.me)

Pokedex AI is a full‑stack AI‑powered Pokémon assistant built with Flask, React, and an OpenAI‑driven NLP classifier.

The system provides structured, game‑accurate Pokémon data through natural‑language queries. It supports move details, offensive and defensive type matchups (including dual‑type combinations), Pokémon summaries, ability information (including hidden abilities), and complete evolution chains. The project emphasizes clean API design, real Pokémon mechanics, and a conversational interface.

---

## Deployment

Pokedex AI is deployed using a split‑service architecture:

- Frontend  
  Hosted on Vercel  
  https://pokedexai.me

- Backend API  
  Hosted on Render  
  https://api.pokedexai.me

This service powers all data retrieval, NLP routing, PokéAPI normalization, and structured responses.

The live deployment reflects the current state of the project and updates automatically as new features are pushed to the main branch.

---

## Features (Current)

### Natural Language Querying

The assistant interprets user questions and routes them to the correct backend endpoint. Supported queries include:

- Move details
- Pokémon summaries
- Offensive type matchups
- Defensive type matchups
- Dual‑type offensive and defensive matchups
- Ability information
- Complete evolution chains
- Smalltalk

The NLP classifier extracts entities such as Pokémon names, move names, ability names, and types (single or dual).

---

### Move Information

The backend returns structured move data:

- Type
- Category (physical, special, status)
- Power (omitted for status moves)
- Accuracy
- Effect text

Move descriptions automatically adjust based on category.

---

### Type Matchups (Offense + Defense)

Supports full matchup reasoning for both **offense** and **defense**, including dual‑type combinations.

#### Defensive Examples:

- “What is Fire weak to”
- “What hits Water super effectively”
- “What is Tyranitar weak to”

#### Offensive Examples:

- “What is Fire effective against”
- “What resists Electric”
- “What does Charizard hit”

#### Dual‑Type Examples:

- “What is Fire/Dark weak to”
- “What does Water/Flying hit”
- “What resists Steel/Fairy”

Dual‑type logic is implemented through type‑combination functions for both offense and defense.

---

### Ability Information

For any Pokémon:

- Lists all abilities
- Labels hidden abilities
- Includes effect descriptions

For any ability:

- Returns the ability’s effect text

---

### Evolution Chains (Complete)

All evolution methods from the PokéAPI are now fully supported, including:

- Level‑based evolutions
- Item‑based evolutions
- Time‑of‑day evolutions
- Friendship evolutions (e.g., Riolu, Eevee → Sylveon)
- Location‑based evolutions (e.g., Leafeon, Glaceon)
- Move‑type evolutions (e.g., Sylveon)
- Gender‑specific evolutions
- Trade evolutions
- Trade‑with‑item evolutions
- Stat‑based evolutions (e.g., Attack > Defense)
- Overworld‑weather evolutions
- Step‑based evolutions
- Move‑usage evolutions
- Region‑specific evolutions
- Form‑specific evolutions
- All special‑case edge conditions

The backend now parses **100% of PokéAPI’s EvolutionDetail fields** and produces clean, human‑readable evolution requirements.

---

### Smalltalk

Handles greetings and simple conversational prompts.

---

## Architecture

- frontend/ → React (Vite) UI
- backend/ → Flask API
- nlp/ → Intent classifier using OpenAI
- pokeapi/ → Wrapper around PokéAPI with normalization helpers

### Backend Endpoints

| Route                     | Description                         |
| ------------------------- | ----------------------------------- |
| `/move/<name>`            | Move details                        |
| `/type/<type>`            | Type matchup data (offense/defense) |
| `/pokemon/<name>`         | Pokémon summary                     |
| `/pokemon-species/<name>` | Evolution chain                     |
| `/ability/<name>`         | Ability details                     |
| `/chat`                   | NLP‑powered chat endpoint           |

---

## NLP Intent Classification

The classifier identifies:

- `move_info`
- `pokemon_info`
- `pokemon_offense`
- `pokemon_defense`
- `offensive_type_matchup`
- `defensive_type_matchup`
- `dual_type_offensive_matchup`
- `dual_type_defensive_matchup`
- `ability_info`
- `evolution_chain`
- `smalltalk`
- `unknown`

It extracts:

- Pokémon names
- Move names
- Ability names
- Types (single or dual, strictly JSON arrays for dual types)

The classifier includes logic for:

- Pokémon ability queries
- Dual‑type extraction
- Offensive vs defensive phrasing
- Unknown intent fallthrough
- Avoiding misclassification of subjective comparisons  
  (e.g., “Is fire better than water” → unknown)

---

## Installation

Backend:

- cd backend
- pip install -r requirements.txt
- python app.py

Frontend:

- cd frontend
- npm install
- npm run dev

---

## Roadmap

### Medium Priority

- Fuzzy matching and spell correction
- Improved evolution chain formatting
- Additional move metadata
- Add regional gimmicks (mega, dynamax, z-moves, tera)

### Future Enhancements

- Team builder mode
- Competitive analysis tools
- Voice input

---
