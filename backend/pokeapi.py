import requests
import copy
from functools import lru_cache

BASE_URL = "https://pokeapi.co/api/v2"
REGIONAL_SUFFIXES = ["hisui", "galar", "alola", "paldea"]

sprite_cache = {}

def fetch_json(url):
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError(f"Request failed ({res.status_code}): {url}")
    return res.json()

def safe_name(obj):
    return obj["name"] if isinstance(obj, dict) and "name" in obj else None

def normalize(name):
    return name.lower().replace(" ", "-")

def get_english_entry(entries, key):
    for entry in entries:
        if entry["language"]["name"] == "en":
            return entry.get(key)
    return None

@lru_cache(maxsize=256)
def get_sprite(name):
    p = get_pokemon(name)
    s = p["sprites"]

    return (
        s.get("front_default")
        or s["other"]["official-artwork"].get("front_default")
        or s["other"]["home"].get("front_default")
    )

def format_evo_details(d):
    parts = []

    # Trigger
    if d.get("trigger"):
        parts.append(d["trigger"].replace("-", " ").title())

    # Level
    if d.get("min_level"):
        parts.append(f"Level {d['min_level']}")

    # Items
    if d.get("item"):
        parts.append(f"Use {d['item'].replace('-', ' ').title()}")
    if d.get("held_item"):
        parts.append(f"Holding {d['held_item'].replace('-', ' ').title()}")

    # Moves
    if d.get("known_move"):
        parts.append(f"Knows move {d['known_move'].title()}")
    if d.get("known_move_type"):
        parts.append(f"Knows a {d['known_move_type'].title()}-type move")

    # Location
    if d.get("location"):
        parts.append(f"At {d['location'].replace('-', ' ').title()}")

    # Friendship / beauty / affection
    if d.get("min_happiness"):
        parts.append(f"Happiness ≥ {d['min_happiness']}")
    if d.get("min_beauty"):
        parts.append(f"Beauty ≥ {d['min_beauty']}")
    if d.get("min_affection"):
        parts.append(f"Affection ≥ {d['min_affection']}")

    # Weather
    if d.get("needs_overworld_rain"):
        parts.append("While raining")

    # Party requirements
    if d.get("party_species"):
        parts.append(f"With {d['party_species'].title()} in party")
    if d.get("party_type"):
        parts.append(f"With a {d['party_type'].title()}-type in party")

    # Stats
    if d.get("relative_physical_stats") == 1:
        parts.append("Attack > Defense")
    elif d.get("relative_physical_stats") == 0:
        parts.append("Attack = Defense")
    elif d.get("relative_physical_stats") == -1:
        parts.append("Attack < Defense")

    # Time of day
    if d.get("time_of_day"):
        parts.append(d["time_of_day"].title())

    # Trade
    if d.get("trade_species"):
        parts.append(f"Trade for {d['trade_species'].title()}")
    elif d.get("trigger") == "trade":
        parts.append("Trade")

    # Special triggers
    if d.get("turn_upside_down"):
        parts.append("Turn console upside-down")
    if d.get("needs_multiplayer"):
        parts.append("Multiplayer required")

    # Region / form
    if d.get("region"):
        parts.append(f"In {d['region'].title()}")
    if d.get("base_form"):
        parts.append(f"Must be in form {d['base_form'].title()}")

    # Move usage
    if d.get("used_move"):
        parts.append(f"Use move {d['used_move'].title()}")
    if d.get("min_move_count"):
        parts.append(f"Use move {d['min_move_count']} times")

    # Steps / damage
    if d.get("min_steps"):
        parts.append(f"Walk {d['min_steps']} steps")
    if d.get("min_damage_taken"):
        parts.append(f"Take {d['min_damage_taken']} damage")

    return ", ".join(parts) if parts else None

def parse_evolution_chain(chain):
    evolutions = []

    def walk(node):
        base_species = node["species"]["name"]

        for evo in node["evolves_to"]:
            to_species = evo["species"]["name"]
            raw = evo["evolution_details"][0] if evo["evolution_details"] else {}
            
            details = {
                "trigger": safe_name(raw.get("trigger")),
                "item": safe_name(raw.get("item")),
                "held_item": safe_name(raw.get("held_item")),
                "known_move": safe_name(raw.get("known_move")),
                "known_move_type": safe_name(raw.get("known_move_type")),
                "location": safe_name(raw.get("location")),
                "party_species": safe_name(raw.get("party_species")),
                "party_type": safe_name(raw.get("party_type")),
                "trade_species": safe_name(raw.get("trade_species")),
                "region": safe_name(raw.get("region")),
                "base_form": safe_name(raw.get("base_form")),
                "used_move": safe_name(raw.get("used_move")),
                "min_level": raw.get("min_level"),
                "min_happiness": raw.get("min_happiness"),
                "min_beauty": raw.get("min_beauty"),
                "min_affection": raw.get("min_affection"),
                "needs_multiplayer": raw.get("needs_multiplayer"),
                "needs_overworld_rain": raw.get("needs_overworld_rain"),
                "relative_physical_stats": raw.get("relative_physical_stats"),
                "time_of_day": raw.get("time_of_day"),
                "min_move_count": raw.get("min_move_count"),
                "min_steps": raw.get("min_steps"),
                "min_damage_taken": raw.get("min_damage_taken"),
            }

            item = details.get("item") or details.get("held_item")

            base_entry = {
                "from": base_species,
                "to": to_species,
                **details, 
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
            evo_node["species"]["sprite"] = get_sprite(target)

            # Find matching flat entry
            match = next((e for e in steps if e["to"] == target), None)

            if match:
                evo_node["details"] = match
                evo_node["details"]["text"] = format_evo_details(match)


            # Add regional forms as extra branches
            regionals = [e for e in steps if e.get("region") and e["to"].startswith(target)]
            if regionals:
                evo_node.setdefault("regional_forms", [])
                for r in regionals:
                    evo_node["regional_forms"].append({
                        "species": {"name": r["to"], "sprite": get_sprite(r["to"])},
                        "details": r,
                        "text": format_evo_details(r)
                    })

            walk(evo_node)

    chain["species"]["sprite"] = get_sprite(chain["species"]["name"])
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

def combine_offense_type_matchups(types):
    merged = {
        "super_effective": set(),
        "not_very_effective": set(),
        "no_effect": set()
    }

    for t in types:
        rel = get_offensive_matchups(t)
        merged["super_effective"].update(rel["super_effective"])
        merged["not_very_effective"].update(rel["not_very_effective"])
        merged["no_effect"].update(rel["no_effect"])

    return {
        "super_effective": sorted(merged["super_effective"]),
        "not_very_effective": sorted(merged["not_very_effective"]),
        "no_effect": sorted(merged["no_effect"]),
    }

def get_offensive_matchups(attacking_type):
    t = get_type(attacking_type)
    rel = t["damage_relations"]

    return {
        "super_effective": [x["name"] for x in rel["double_damage_to"]],
        "not_very_effective": [x["name"] for x in rel["half_damage_to"]],
        "no_effect": [x["name"] for x in rel["no_damage_to"]],
    }

def get_defensive_matchups(defensive_type):
    t = get_type(defensive_type)
    rel = t["damage_relations"]

    return {
        "double_damage_from": [x["name"] for x in rel["double_damage_from"]],
        "half_damage_from": [x["name"] for x in rel["half_damage_from"]],
        "no_damage_from": [x["name"] for x in rel["no_damage_from"]],
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
