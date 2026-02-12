from dotenv import load_dotenv 
from openai import OpenAI 
import json

load_dotenv() 
client = OpenAI()

def classify_intent(user_message):
    system_prompt = """
        You classify user messages into Pokémon-related intents.

        Valid Pokémon types are:
        normal, fire, water, grass, electric, ice, fighting, poison,
        ground, flying, psychic, bug, rock, ghost, dragon, dark,
        steel, fairy.

        Your job is to identify:
        - what the user is asking about
        - which entity (move, Pokémon, type, or ability) they mean

        You MUST follow these rules:

        1. MOVE INFO
        If the user mentions a move name (e.g. "thunderbolt", "use flamethrower",
        "what does ice punch do"), classify as "move_info".
        The entity MUST be the move name in lowercase.
        Never return null for a move.

        If the user says “fire type move”, “electric move”, etc. but does NOT name
        a specific move, this is NOT move_info — it is a type matchup question.

        2. TYPE MATCHUP
        If the user asks about:
        - weaknesses
        - resistances
        - effectiveness
        - "what hits X"
        - "what resists X"
        - "what is X weak to"
        - "what is X strong against"
        - "fire type move is effective against"
        - "what is effective on ghost dark"
        - "what does fire hit"
        - "what takes reduced damage from fire"

        classify as "type_matchup".

        Extract all valid types mentioned.
        If one type appears → entity is ["fire"]
        If two types appear → entity is ["ghost", "dark"]

        If the user names a Pokémon instead of types (e.g. "what is Tyranitar weak to"),
        classify as "type_matchup" and set entity to the Pokémon name.

        If the user compares types using subjective language 
        ("better than", "stronger than", "which is better"), 
        classify as "unknown".


        3. POKÉMON INFO
        If the user asks about a Pokémon in general (e.g. "tell me about pikachu",
        "what type is charizard", "show me bulbasaur"), classify as "pokemon_info".
        Entity is the Pokémon name in lowercase.

        Do NOT use pokemon_info if the question is specifically about abilities,
        weaknesses, resistances, or evolutions.

        4. ABILITY INFO
        If the user mentions an ability name (e.g. "levitate", "intimidate",
        "what does pressure do"), classify as "ability_info".
        The entity MUST be the ability name in lowercase.
        Never return null for an ability.

        If the user asks for the ability of a Pokémon (e.g.
        "what is charmander's ability",
        "what ability does pikachu have",
        "tell me bulbasaur's abilities"),
        classify as "ability_info" and set entity to the Pokémon name in lowercase.

        5. EVOLUTION
        If the user asks how a Pokémon evolves, classify as "evolution_chain".
        Entity is the Pokémon name in lowercase.

        6. SMALLTALK
        Greetings or casual chat → "smalltalk".

        7. UNKNOWN
        If unclear → "unknown".

        Respond ONLY with JSON:
        {
        "intent": "...",
        "entity": ...
        }


        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return json.loads(response.choices[0].message.content)