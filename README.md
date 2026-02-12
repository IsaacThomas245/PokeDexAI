# Pokedex AI

Pokedex AI is a full‑stack AI‑powered Pokémon assistant built with Flask, React, and an OpenAI‑driven NLP classifier.

The system provides structured, game‑accurate Pokémon data through natural‑language queries. It supports move details, defensive type matchups, Pokémon summaries, ability information (including hidden abilities), and basic evolution chains. The project emphasizes clean API design, real Pokémon mechanics, and a conversational interface.

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

## Features (Current)

### Natural Language Querying
The assistant interprets user questions and routes them to the correct backend endpoint. Supported queries include:
- Move details
- Pokémon summaries
- Defensive type matchups
- Ability information
- Basic evolution chains
- Smalltalk

The NLP classifier extracts entities such as Pokémon names, move names, ability names, and types.

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

### Defensive Type Matchups
Currently supports defensive matchup reasoning:
- “What is Fire weak to”
- “What resists Water”
- “What is Tyranitar weak to”

Dual‑type defensive logic is implemented through a type‑combination function.

Note: Offensive matchup reasoning (e.g., “What does Fire hit super effectively”) is not yet implemented.

---

### Ability Information
For any Pokémon:
- Lists all abilities
- Labels hidden abilities
- Includes effect descriptions

For any ability:
- Returns the ability’s effect text

---

### Evolution Chains (Basic)
Supports:
- Level‑based evolutions
- Item‑based evolutions
- Time‑of‑day evolutions

Not yet implemented:
- Friendship evolutions (Riolu, Eevee → Sylveon)
- Location evolutions (Leafeon, Glaceon)
- Move‑type evolutions (Sylveon)

These are planned improvements.

---

### Smalltalk
Handles greetings and simple conversational prompts.

---

## Architecture
- frontend/     → React (Vite) UI
- backend/      → Flask API
- nlp/          → Intent classifier using OpenAI
- pokeapi/      → Wrapper around PokéAPI with normalization helpers


### Backend Endpoints

| Route | Description |
|-------|-------------|
| `/move/<name>` | Move details |
| `/type/<type>` | Defensive type matchup data |
| `/pokemon/<name>` | Pokémon summary |
| `/pokemon-species/<name>` | Evolution chain |
| `/ability/<name>` | Ability details |
| `/chat` | NLP‑powered chat endpoint |

---

## NLP Intent Classification

The classifier identifies:
- `move_info`
- `pokemon_info`
- `type_matchup` (defensive only)
- `ability_info`
- `evolution_chain`
- `smalltalk`
- `unknown`

It extracts:
- Pokémon names
- Move names
- Ability names
- Types (single or dual)

The classifier includes logic for:
- Pokémon ability queries
- Dual‑type extraction
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

### High Priority
- Offensive type matchup reasoning
- Friendship evolutions
- Location‑based evolutions
- Move‑type evolutions

### Medium Priority
- Fuzzy matching and spell correction
- Improved evolution chain formatting
- Additional move metadata

### Future Enhancements
- Team builder mode
- Competitive analysis tools
- Voice input

---
