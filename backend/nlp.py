from dotenv import load_dotenv 
from openai import OpenAI 
import json

load_dotenv() 
client = OpenAI()

def classify_intent(user_message):
    system_prompt = """
        You classify user messages into Pokémon-related intents. 
        Respond ONLY with valid JSON in this format:
        {"intent": "...", "entity": ...}

        INTENTS:
        - move_info → user asks about a move (e.g. “thunderbolt”, “what does flamethrower do”)
        entity = move name (string)

        - pokemon_info → user asks about a Pokémon's info or type (e.g. “what type is pikachu”)
        entity = Pokémon name (string)

        - offensive_type_matchup → user asks what a type is good against OR what resists that type
        entity = type (string)

        - defensive_type_matchup → user asks what a type is weak to OR what hits it super effectively
        entity = type (string)

        - dual_type_offensive_matchup → same as offensive but with TWO types
        entity = ["type1", "type2"]

        - dual_type_defensive_matchup → same as defensive but with TWO types
        entity = ["type1", "type2"]

        - pokemon_offense → user asks what a Pokémon is good against
        entity = Pokémon name (string)

        - pokemon_defense → user asks what a Pokémon is weak to
        entity = Pokémon name (string)

        - ability_info → user asks about an ability OR a Pokémon's abilities
        entity = ability or Pokémon name (string)

        - evolution_chain → user asks how a Pokémon evolves
        entity = Pokémon name (string)

        - smalltalk → greetings or casual chat (“hi”, “hello”, “what's up”)

        - unknown → anything else

        RULES:
        - Types must be lowercase.
        - Dual types must be a JSON array of two strings.
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
