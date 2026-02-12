import requests
import copy

BASE_URL = "https://pokeapi.co/api/v2"
REGIONAL_SUFFIXES = ["hisui", "galar", "alola", "paldea"]

def fetch_json(url):
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError(f"Request failed ({res.status_code}): {url}")
    return res.json()

def normalize(name):
    return name.lower().replace(" ", "-")

def get_english_entry(entries, key):
    for entry in entries:
        if entry["language"]["name"] == "en":
            return entry.get(key)
    return None

def format_evo_details(details):
    if not details:
        return None

    trigger = details.get("trigger")
    item = details.get("item")
    level = details.get("min_level")
    time = details.get("time_of_day")

    # Trade evolutions
    if trigger == "trade":
        if item:
            return f"Trade while holding {item.replace('-', ' ').title()}"
        return "Trade"

    # Level evolutions
    if level:
        return f"Level {level}"

    # Item evolutions
    if item:
        return f"Use {item.replace('-', ' ').title()}"

    # Time of day evolutions
    if time:
        return f"At {time.title()}"

    return None

def parse_evolution_chain(chain):
    evolutions = []

    def walk(node):
        base_species = node["species"]["name"]

        for evo in node["evolves_to"]:
            to_species = evo["species"]["name"]
            details = evo["evolution_details"][0] if evo["evolution_details"] else {}

            item = None
            if details.get("item"):
                item = details["item"]["name"]
            elif details.get("held_item"):
                item = details["held_item"]["name"]


            base_entry = {
                "from": base_species,
                "to": to_species,
                "trigger": details.get("trigger", {}).get("name"),
                "min_level": details.get("min_level"),
                "item": item,
                "time_of_day": details.get("time_of_day"),
            }


            evolutions.append(base_entry)

            regional_forms = get_available_forms(to_species)
            for region in regional_forms:
                evolutions.append({
                    **base_entry,
                    "to": f"{to_species}-{region}",
                    "region": region
                })

            walk(evo)

    walk(chain)
    return evolutions

def merge_evolution_data(chain, flat):
    def walk(node):
        species = node["species"]["name"]

        # Find all evolutions from this species in the flat list
        steps = [e for e in flat if e["from"] == species]

        # Attach details to each evolves_to entry
        for evo_node in node.get("evolves_to", []):
            target = evo_node["species"]["name"]

            # Find matching flat entry
            match = next((e for e in steps if e["to"] == target), None)

            if match:
                evo_node["details"] = {
                    "trigger": match["trigger"],
                    "min_level": match["min_level"],
                    "item": match["item"],
                    "time_of_day": match["time_of_day"]
                }
                evo_node["details"]["text"] = format_evo_details(evo_node["details"])

            # Add regional forms as extra branches
            regionals = [e for e in steps if e.get("region") and e["to"].startswith(target)]
            if regionals:
                evo_node.setdefault("regional_forms", [])
                for r in regionals:
                    evo_node["regional_forms"].append({
                        "species": {"name": r["to"]},
                        "details": {
                            "trigger": r["trigger"],
                            "min_level": r["min_level"],
                            "item": r["item"],
                            "time_of_day": r["time_of_day"],
                            "region": r["region"],
                        }
                    })

            walk(evo_node)

    walk(chain)
    return chain


def get_available_forms(species_name):
    forms = []

    for region in REGIONAL_SUFFIXES:
        try:
            fetch_json(f"{BASE_URL}/pokemon/{species_name}-{region}")
            forms.append(region)
        except ValueError:
            pass

    return forms

def combine_type_matchups(types):
    multipliers = {}

    for t in types:
        data = get_type(t)
        relations = data["damage_relations"]

        for target in relations["double_damage_from"]:
            multipliers[target["name"]] = multipliers.get(target["name"], 1) * 2

        for target in relations["half_damage_from"]:
            multipliers[target["name"]] = multipliers.get(target["name"], 1) * 0.5

        for target in relations["no_damage_from"]:
            multipliers[target["name"]] = multipliers.get(target["name"], 1) * 0

    # Now categorize by multiplier
    result = {
        "quadruple_weak_to": [t for t, m in multipliers.items() if m == 4],
        "double_weak_to":    [t for t, m in multipliers.items() if m == 2],
        "neutral":           [t for t, m in multipliers.items() if m == 1],
        "half_resistant_to": [t for t, m in multipliers.items() if m == 0.5],
        "quarter_resistant_to": [t for t, m in multipliers.items() if m == 0.25],
        "immune_to":         [t for t, m in multipliers.items() if m == 0],
    }

    return result

# for answering questions like "what is effective against tyranitar"
def get_offensive_matchups(attacking_type):
    t = get_type(attacking_type)
    rel = t["damage_relations"]

    return {
        "super_effective": [x["name"] for x in rel["double_damage_to"]],
        "not_very_effective": [x["name"] for x in rel["half_damage_to"]],
        "no_effect": [x["name"] for x in rel["no_damage_to"]],
    }


def get_pokemon(name):
    normalized = normalize(name)

    try:
        return fetch_json(f"{BASE_URL}/pokemon/{normalized}")
    except ValueError:
        for suffix in REGIONAL_SUFFIXES:
            new_suffix = "-" + suffix
            if normalized.endswith(new_suffix):
                base_name = normalized.replace(new_suffix, "")
                return fetch_json(f"{BASE_URL}/pokemon/{base_name}")
        raise

def get_move(name):
    return fetch_json(f"{BASE_URL}/move/{normalize(name)}")

def get_type(name):
    return fetch_json(f"{BASE_URL}/type/{normalize(name)}")

def get_ability(name):
    return fetch_json(f"{BASE_URL}/ability/{normalize(name)}")

def get_pokemon_abilities(pokemon_name):
    data = get_pokemon(pokemon_name)
    return [a["ability"]["name"] for a in data["abilities"]]

def get_ability_effect(ability_name):
    data = get_ability(ability_name)
    return get_english_entry(data["effect_entries"], "short_effect")

def get_move_effect(move):
    effect = get_english_entry(move.get("effect_entries", []), "short_effect")
    if effect:
        return effect

    flavor = get_english_entry(move.get("flavor_text_entries", []), "flavor_text")
    if flavor:
        return flavor.replace("\n", " ")

    return "No effect description available."

def get_evolution_chain(pokemon_name):
    pokemon = get_pokemon(pokemon_name)
    species_url = pokemon["species"]["url"]

    species = fetch_json(species_url)
    evo_chain_url = species["evolution_chain"]["url"]

    evo_chain = fetch_json(evo_chain_url)

    flat = parse_evolution_chain(evo_chain["chain"])

    chain_copy = copy.deepcopy(evo_chain["chain"])

    merged = merge_evolution_data(chain_copy, flat)

    return merged
