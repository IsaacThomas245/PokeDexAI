from dotenv import load_dotenv 
from openai import OpenAI 
import json

load_dotenv() 
client = OpenAI()

def classify_intent(user_message):
    system_prompt = """
        You classify user messages into Pokémon-related intents.
        Respond ONLY with valid JSON in this exact format:
        {"intent": "...", "entity": ...}

        INTENTS
        -------

        move_info  
        User asks about a move.
        Examples: “thunderbolt”, “what does flamethrower do”
        entity = move name (string)

        pokemon_info  
        User asks about a Pokémon's info, identity, description, or type.
        Includes:
        - “what type is pikachu”
        - “tell me about bulbasaur”
        - “who is charizard”
        - “who is slowking”
        - “who is galarian slowking”
        - “what is mewtwo”
        - “describe greninja”
        entity = Pokémon name (string, lowercase)

        offensive_type_matchup  
        User asks what a type is good against OR what resists that type.
        Examples: “what is fire good against”, “what resists electric”
        entity = type (string, lowercase)

        defensive_type_matchup  
        User asks what a type is weak to OR what hits it super effectively.
        Examples: “what is fire weak to”, “what hits water super effectively”
        entity = type (string, lowercase)

        dual_type_offensive_matchup  
        Same as offensive, but with two types.
        Examples: “what does fire dark hit”, “what resists steel fairy”
        entity = ["type1", "type2"]

        dual_type_defensive_matchup  
        Same as defensive, but with two types.
        Examples: “what is steel fairy weak to”, “what hurts bug steel”
        entity = ["type1", "type2"]

        pokemon_offense  
        User asks what a Pokémon is good against.
        Examples: “what does charizard hit”, “what is lucario good against”
        entity = Pokémon name (string)

        pokemon_defense  
        User asks what a Pokémon is weak to.
        Examples: “what is charizard weak to”, “what hurts garchomp”
        entity = Pokémon name (string)

        ability_info  
        User asks about an ability OR a Pokémon's abilities.
        Examples: “what does levitate do”, “what abilities does bulbasaur have”
        entity = ability or Pokémon name (string)

        evolution_chain  
        User asks how a Pokémon evolves.
        Examples: “how does eevee evolve”, “what does charmander evolve into”
        entity = Pokémon name (string)

        smalltalk  
        Greetings or casual chat.
        Examples: “hi”, “hello”, “what's up”

        unknown  
        Anything else, including:
        - type comparisons (“is fire better than water”)
        - battle hypotheticals (“who would win charizard or blastoise”)
        - non-Pokémon questions

        RULES
        -----
        - Types must be lowercase.
        - Dual types must be a JSON array of two strings.
        - Pokémon names must be lowercase.
        - NEVER include explanations.
        - NEVER include extra text.
        - ONLY output the JSON object.

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
