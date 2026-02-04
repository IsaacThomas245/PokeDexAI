from flask import Flask, request, jsonify
from flask_cors import CORS
from pokeapi import get_move, get_move_effect, get_type, get_pokemon, get_ability, get_ability_effect, get_evolution_chain

app = Flask(__name__)
CORS(app)

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

@app.route("/pokemon/<name>")
def pokemon_summary(name):
    p = get_pokemon(name)
    return {
        "types": [t["type"]["name"] for t in p["types"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in p["stats"]},
        "abilities": [a["ability"]["name"] for a in p["abilities"]],
        "moves": [m["move"]["name"] for m in p["moves"]]
    }

@app.route("/pokemon-species/<name>")
def pokemon_evolution(name):
    p = get_evolution_chain(name)
    return p

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

    return jsonify({
        "role": "assistant",
        "content": "Thunderbolt is a powerful Electric-type move.",
        "type": "move",
        "data": {
            "name": "Thunderbolt",
            "power": 90,
            "accuracy": 100,
            "type": "electric",
            "category": "special",
            "effect": "May paralyze the target."
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
