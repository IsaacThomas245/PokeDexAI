from flask import Flask, request, jsonify
from flask_cors import CORS
from pokeapi import get_move, get_move_effect, get_type, get_pokemon, get_ability, get_ability_effect, get_evolution_chain, combine_type_matchups
from nlp import classify_intent

app = Flask(__name__)
CORS(app)

# Given the name of a move, return details about the move
@app.route("/move/<name>")
def move_info(name):
    move = get_move(name)

    return {
        "name": move["name"],
        "power": move["power"],
        "accuracy": move["accuracy"],
        "type": move["type"]["name"],
        "category": move["damage_class"]["name"],
        "effect": get_move_effect(move)
    }

# given a type, return damage relations of the type
@app.route("/type/<type>")
def type_matchups(type):
    data = get_type(type)
    return { 
        "double_damage_to": [t["name"] for t in data["damage_relations"]["double_damage_to"]], 
        "double_damage_from": [t["name"] for t in data["damage_relations"]["double_damage_from"]], 
        "half_damage_to": [t["name"] for t in data["damage_relations"]["half_damage_to"]], 
        "half_damage_from": [t["name"] for t in data["damage_relations"]["half_damage_from"]], 
        "no_damage_to": [t["name"] for t in data["damage_relations"]["no_damage_to"]], 
        "no_damage_from": [t["name"] for t in data["damage_relations"]["no_damage_from"]], 
    }

# given a pokemon name, return type, stats, abiities, and move list
@app.route("/pokemon/<name>")
def pokemon_summary(name):
    p = get_pokemon(name)
    return {
        "types": [t["type"]["name"] for t in p["types"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in p["stats"]},
        "abilities": [a["ability"]["name"] for a in p["abilities"]],
        "moves": [m["move"]["name"] for m in p["moves"]]
    }

# given a pokemon name, return its evolution line
@app.route("/pokemon-species/<name>")
def pokemon_evolution(name):
    p = get_evolution_chain(name)
    return jsonify(p)

# given an ability, return description of the ability
@app.route("/ability/<name>") 
def ability_info(name): 
    ability = get_ability(name) 
    ability_effect = get_ability_effect(name)
    return { 
        "name": ability["name"], "effect": ability_effect 
    }

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message")

    print("Received:", user_message)

    # process intent and entity gotten from nlp
    intent_data = classify_intent(user_message)
    intent = intent_data["intent"]
    entity = intent_data["entity"]

    print(intent)
    print(entity)

    if intent == "move_info":
        move = get_move(entity)
        if move["damage_class"]["name"] != "physical" or move["damage_class"]["name"] != "special":
            return jsonify({
            "role": "assistant",
            "content": f"{entity.title()} is a {move['type']['name']}-type {move["damage_class"]["name"]} move.",
            "type": "move",
            "data": {
                "name": move["name"],
                "power": move["power"],
                "accuracy": move["accuracy"],
                "type": move["type"]["name"],
                "category": move["damage_class"]["name"],
                "effect": get_move_effect(move)
            }
        })

        return jsonify({
            "role": "assistant",
            "content": f"{entity.title()} is a {move['type']['name']}-type {move["damage_class"]["name"]} move with {move['power']} power.",
            "type": "move",
            "data": {
                "name": move["name"],
                "power": move["power"],
                "accuracy": move["accuracy"],
                "type": move["type"]["name"],
                "category": move["damage_class"]["name"],
                "effect": get_move_effect(move)
            }
        })

    elif intent == "pokemon_info":
        p = get_pokemon(entity)
        return jsonify({
            "role": "assistant",
            "content": f"{entity.title()} is a {', '.join(t['type']['name'] for t in p['types'])}-type Pokémon.",
            "type": "pokemon",
            "data": {
                "types": [t["type"]["name"] for t in p["types"]],
                "stats": {s["stat"]["name"]: s["base_stat"] for s in p["stats"]},
                "abilities": [a["ability"]["name"] for a in p["abilities"]],
                "moves": [
                    {
                        "name": m["move"]["name"],
                        "level": m["version_group_details"][0]["level_learned_at"],
                        "method": m["version_group_details"][0]["move_learn_method"]["name"]
                    }
                    for m in p["moves"]
                ]
            }
        })

    elif intent == "type_matchup":
        # case for dual type matchup(ex: weaknesses of a ghost/dark pokemon)
        if isinstance(entity, list):
            combined = combine_type_matchups(entity)
            return jsonify({
                "role": "assistant",
                "content": f"{' / '.join(t.title() for t in entity)} type matchup:",
                "type": "type",
                "data": combined
            })

        # Otherwise, entity is either a pokemon or a single type
        try:
            # Try treating entity as a type
            t = get_type(entity)
            return jsonify({
                "role": "assistant",
                "content": f"{entity.title()} type strengths and weaknesses:",
                "type": "type",
                "data": {
                    "double_damage_to": [x["name"] for x in t["damage_relations"]["double_damage_to"]],
                    "double_damage_from": [x["name"] for x in t["damage_relations"]["double_damage_from"]],
                    "half_damage_to": [x["name"] for x in t["damage_relations"]["half_damage_to"]],
                    "half_damage_from": [x["name"] for x in t["damage_relations"]["half_damage_from"]],
                    "no_damage_to": [x["name"] for x in t["damage_relations"]["no_damage_to"]],
                    "no_damage_from": [x["name"] for x in t["damage_relations"]["no_damage_from"]],
                }
            })
        except:
            pass

        # Otherwise treat entity as a Pokémon
        p = get_pokemon(entity)
        types = [t["type"]["name"] for t in p["types"]]
        combined = combine_type_matchups(types)

        return jsonify({
            "role": "assistant",
            "content": f"{entity.title()} is {', '.join(types)} type. Here are its weaknesses and resistances:",
            "type": "type",
            "data": combined
        })

    elif intent == "ability_info":
        # entity is either an ability or pokemon, try assuming entity is an ability
        try:
            ability_data = get_ability(entity)
            effect = get_ability_effect(entity)

            return jsonify({
                "role": "assistant",
                "content": f"Ability: {entity.title()}",
                "type": "ability",
                "data": {
                    "name": entity,
                    "effect": effect
                }
            })
        except:
            pass 

        # Otherwise, entity is a Pokemon
        p = get_pokemon(entity)
        ability_names = [a["ability"]["name"] for a in p["abilities"]]
        ability_hidden = [a["is_hidden"] for a in p["abilities"]]

        abilities = []
        for i in range(len(ability_names)):
            ability_name = ability_names[i]
            ability_is_hidden = ability_hidden[i]
            effect = get_ability_effect(ability_name)
            final_name = ability_name
            if ability_is_hidden:
                final_name += " (hidden ability)"
            else:
                final_name += " (normal ability)"

            abilities.append({
                "name": final_name,
                "effect": effect,
            })

        return jsonify({
            "role": "assistant",
            "content": f"{entity.title()} has the abilities: {', '.join(ability_names)}.",
            "type": "ability",
            "data": abilities
        })


    elif intent == "evolution_chain":
        evo = get_evolution_chain(entity)
        return jsonify({
            "role": "assistant",
            "content": f"Here is the evolution chain for {entity.title()}.",
            "type": "evolution",
            "data": evo
        })
    
    elif intent == "smalltalk":
        return jsonify({
            "role": "assistant",
            "content": "Hey! Ask me about any Pokémon, move, type, ability, or evolution.",
            "type": "text",
            "data": None
        })
    
    else:
        return jsonify({
        "role": "assistant",
        "content": "I'm not sure what you meant. Try asking about a Pokémon, move, type, or ability.",
        "type": "error",
        "data": None
    })


if __name__ == "__main__":
    app.run(debug=True)
