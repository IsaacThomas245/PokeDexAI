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
        - the user's intent
        - the correct entity (type, Pokémon, move, or ability)

        You MUST follow these rules exactly:

        ------------------------------------------------------------
        GENERAL JSON RULES (STRICT)
        ------------------------------------------------------------
        1. Your response MUST be valid JSON.
        2. "entity" MUST match the required JSON type for the intent.
        3. For dual-type intents, "entity" MUST be a JSON array of two
        separate strings, like this:

        "entity": ["fire", "dark"]

        NEVER return:
        - "fire,dark"
        - "fire, dark"
        - ["fire,dark"]
        - "fire/dark"
        - "fire dark"

        4. If the user provides two types in any format, you MUST convert
        them into a JSON array of two lowercase strings.

        ------------------------------------------------------------
        1. MOVE INFO
        ------------------------------------------------------------
        If the user names a specific move (e.g. "thunderbolt",
        "ice punch", "flamethrower"), classify as "move_info".

        Entity = move name in lowercase.

        ------------------------------------------------------------
        2. OFFENSIVE TYPE MATCHUP (single type → offense)
        ------------------------------------------------------------
        Classify as "offensive_type_matchup" when the user asks what a
        TYPE is good *against*, OR what *resists* that type's attacks.

        Offensive phrasing includes:
        - "what is fire effective against"
        - "what does water hit"
        - "what types does electric beat"
        - "what is grass strong against"
        - "what resists electric"
        - "what resists fire"
        - "what takes reduced damage from ice"
        - "what is resistant to fighting moves"

        Entity = single type in lowercase.

        ------------------------------------------------------------
        3. DUAL-TYPE OFFENSIVE MATCHUP (two types → offense)
        ------------------------------------------------------------
        Classify as "dual_type_offensive_matchup" when the user asks what
        a dual-type combination is good *against* OR what *resists* it.

        Examples:
        - "what does fire dark hit"
        - "what is water flying good against"
        - "what resists steel fairy"
        - "what resists ghost poison"

        Entity MUST be a JSON array of two types:
        ["fire", "dark"]

        ------------------------------------------------------------
        4. DEFENSIVE TYPE MATCHUP (single type → defense)
        ------------------------------------------------------------
        Classify as "defensive_type_matchup" when the user asks what a
        TYPE is weak to, or what hits it super effectively.

        Defensive phrasing includes:
        - "what is fire weak to"
        - "what hits water super effectively"
        - "what hurts rock type"
        - "what is steel weak against"
        - "what is psychic weak to"

        IMPORTANT:
        “what resists X” is NOT defensive — it is offensive.

        Entity = single type in lowercase.

        ------------------------------------------------------------
        5. DUAL-TYPE DEFENSIVE MATCHUP (two types → defense)
        ------------------------------------------------------------
        Classify as "dual_type_defensive_matchup" when the user asks what
        a dual-type is weak to or resistant to.

        Examples:
        - "what is fire dark weak to"
        - "what hits steel fairy super effectively"
        - "what hurts bug steel"

        Entity MUST be a JSON array of two types:
        ["fire", "dark"]

        ------------------------------------------------------------
        6. POKÉMON OFFENSE (Pokémon → offense)
        ------------------------------------------------------------
        Classify as "pokemon_offense" when the user asks what a Pokémon
        is good *against*, or what types resist its attacks.

        Examples:
        - "what does charizard hit"
        - "what is lucario good against"
        - "what types does gengar beat"
        - "what resists pikachu's attacks"

        Entity = Pokémon name in lowercase.

        ------------------------------------------------------------
        7. POKÉMON DEFENSE (Pokémon → defense)
        ------------------------------------------------------------
        Classify as "pokemon_defense" when the user asks what a Pokémon
        is weak to or resistant to.

        Examples:
        - "what is charizard weak to"
        - "what hits garchomp super effectively"
        - "what hurts greninja"

        Entity = Pokémon name in lowercase.

        ------------------------------------------------------------
        8. POKÉMON INFO
        ------------------------------------------------------------
        General Pokémon information:

        - "tell me about pikachu"
        - "what type is charizard"
        - "show me bulbasaur"

        Classify as "pokemon_info".

        ------------------------------------------------------------
        9. ABILITY INFO
        ------------------------------------------------------------
        If the user names an ability:

        - "levitate"
        - "intimidate"
        - "what does pressure do"

        Classify as "ability_info".

        If the user asks for a Pokémon's abilities:

        - "what is pikachu's ability"
        - "what abilities does bulbasaur have"

        Entity = Pokémon name in lowercase.

        ------------------------------------------------------------
        10. EVOLUTION
        ------------------------------------------------------------
        If the user asks how a Pokémon evolves:

        - "how does eevee evolve"
        - "what does charmander evolve into"

        Classify as "evolution_chain".

        ------------------------------------------------------------
        11. SMALLTALK
        ------------------------------------------------------------
        Greetings or casual chat → "smalltalk".

        ------------------------------------------------------------
        12. UNKNOWN
        ------------------------------------------------------------
        If unclear, or if the user compares types without asking about
        weaknesses/strengths/effectiveness, classify as "unknown".

        Examples:
        - "which type is better, fire or water"
        - "is ghost stronger than dark"
        - "who would win, charizard or blastoise"

        ------------------------------------------------------------
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

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("BAD JSON FROM MODEL:", raw)
        # fallback to unknown
        return {"intent": "unknown", "entity": None}

def small_talk_response(user_message):
    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly Pokémon-themed assistant. "
                    "Respond with short greetings or light banter. "
                    "You may briefly mention what the user can do on this site "
                    "(for example: ask about Pokémon, moves, types, abilities, or evolutions). "
                    "Keep responses playful and concise. "
                    "Do NOT answer questions, provide factual information, explain mechanics, "
                    "solve tasks, or perform any kind of reasoning. "
                    "If the user asks for information or tries to get help with anything beyond smalltalk, "
                    "do NOT answer it — instead, gently redirect them by saying they can ask about Pokémon, "
                    "moves, types, abilities, or evolutions. "
                    "Stay strictly in smalltalk mode."
                )
            },
            {"role": "user", "content": user_message}
        ]
    )

    return reply.choices[0].message.content
