import requests

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

def parse_evolution_chain(chain):
    evolutions = []

    def walk(node):
        base_species = node["species"]["name"]

        for evo in node["evolves_to"]:
            to_species = evo["species"]["name"]
            details = evo["evolution_details"][0] if evo["evolution_details"] else {}

            base_entry = {
                "from": base_species,
                "to": to_species,
                "trigger": details.get("trigger", {}).get("name"),
                "min_level": details.get("min_level"),
                "item": details.get("item", {}).get("name") if details.get("item") else None,
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

def get_available_forms(species_name):
    forms = []

    for region in REGIONAL_SUFFIXES:
        try:
            fetch_json(f"{BASE_URL}/pokemon/{species_name}-{region}")
            forms.append(region)
        except ValueError:
            pass

    return forms

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
    return parse_evolution_chain(evo_chain["chain"])

