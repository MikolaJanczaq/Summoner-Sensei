import json
import re
import sqlite3
import requests
import sqlite_vec

from config.urls import BASE_URL
from sentence_transformers import SentenceTransformer

# Model for embeddings
encoder = SentenceTransformer('all-MiniLM-L6-v2')

def build_database():
    conn = sqlite3.connect("lol_data.db")

    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS champions (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        key INTEGER NOT NULL UNIQUE,
                        tags TEXT NOT NULL,
                        partype TEXT NOT NULL,
                        hp REAL NOT NULL,
                        hpperlevel REAL NOT NULL,
                        movespeed REAL NOT NULL,
                        armor REAL NOT NULL,
                        armorperlevel REAL NOT NULL,
                        spellblock REAL NOT NULL,
                        spellblockperlevel REAL NOT NULL,
                        attackrange REAL NOT NULL,
                        attackdamage REAL NOT NULL,
                        attackdamageperlevel REAL NOT NULL,
                        attackspeed REAL NOT NULL,
                        attackspeedperlevel REAL NOT NULL,
                        allytips TEXT,
                        enemytips TEXT
                     )""")

    c.execute("""CREATE TABLE IF NOT EXISTS spells (
                        champion_id TEXT NOT NULL,
                        spell_key TEXT NOT NULL,
                        name TEXT NOT NULL,
                        description TEXT,
                        cooldown TEXT,
                        cost TEXT,
                        range TEXT,
                        PRIMARY KEY (champion_id, spell_key),
                        FOREIGN KEY (champion_id) REFERENCES champions (id) ON DELETE CASCADE
                     )""")

    c.execute("""CREATE TABLE IF NOT EXISTS items (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        plaintext TEXT,
                        description TEXT,
                        total_gold INTEGER,
                        tags TEXT,
                        stats_json TEXT
                     )""")

    c.execute("""CREATE TABLE IF NOT EXISTS summoner_spells (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        key INTEGER NOT NULL UNIQUE,
                        description TEXT,
                        cooldown TEXT
                     )""")

    c.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_items USING vec0(
                item_id TEXT PRIMARY KEY,
                embedding float[384]
            )
        """)

    conn.commit()
    conn.close()
    print("Database created successfully")

def _clean_html(raw_text: str) -> str:
    if not raw_text:
        return ""
    return re.sub(r'<[^>]+>', '', raw_text)

def _parse_tooltip(tooltip: str, effect_burn: list, vars_list: list) -> str:
    """
    Translates Riots variable ({{ eN}}, {{aN}}) based on the official docs.
    :param tooltip:
    :param effect_burn:
    :param vars_list:
    :return:
    """

    if not tooltip: return ""

    def replace_e(match):
        index = int(match.group(1))
        if effect_burn and index < len(effect_burn) and effect_burn[index] is not None:
            return str(effect_burn[index])
        return "??" # fallback if riot doesn't provide data

    tooltip = re.sub(r'\{\{\s*e(\d+)\s*\}\}', replace_e, tooltip)

    def replace_vars(match):
        var_key = match.group(1)
        if vars_list:
            for v in vars_list:
                if v.get("key") == var_key:
                    coeffs = v.get("coeff", [])
                    if coeffs:
                        # Sometimes the coefficient is a single number, sometimes an array. We simplify it to a string.
                        return "/".join(str(c) for c in coeffs) if len(set(coeffs)) > 1 else str(coeffs[0])
        return "??"

    tooltip = re.sub(r'\{\{\s*([af]\d+)\s*\}\}', replace_vars, tooltip)

    tooltip = re.sub(r'\{\{\s*[^}]+\s*\}\}', '[dependent on stats]', tooltip)

    return _clean_html(tooltip)

def _parse_resource(resource_text: str, cost_burn: str, effect_burn: list) -> str:
    """
    Translates spell cost based on the rule 'Calculating Spell Costs' from Riot docs
    :param resource_text:
    :param cost_burn:
    :param effect_burn:
    :return:
    """
    if not resource_text or resource_text == "None":
        return "No cost"

    resource_text = re.sub(r'\{\{\s*cost\s*\}\}', str(cost_burn), resource_text)

    def replace_e(match):
        index = int(match.group(1))
        if effect_burn and index < len(effect_burn) and effect_burn[index] is not None:
            return str(effect_burn[index])
        return "??"

    resource_text = re.sub(r'\{\{\s*e(\d+)\s*\}\}', replace_e, resource_text)

    return _clean_html(resource_text)

def _get_champions_list():
    all_champs_response = requests.get(f"{BASE_URL}/champion.json").json()
    return all_champs_response["data"]

def _get_champion_details(champion_id: str):
    champion = requests.get(f"{BASE_URL}/champion/{champion_id}.json").json()
    return champion["data"][champion_id]

def fill_champions():
    print("Filling champions table...")
    champions_list = _get_champions_list()
    total_champs = len(champions_list)
    conn = sqlite3.connect("lol_data.db")
    c = conn.cursor()

    for champ_num, champ_id in enumerate(champions_list.keys(), start=1):
        print(f"\rProcessing champs: {champ_num}/{total_champs} [{champ_id}]{' ' * 10}", end="", flush=True)
        current_champ = champions_list[champ_id]
        champ_details = _get_champion_details(champ_id)

        stats = current_champ["stats"]
        tags = ", ".join(current_champ["tags"])
        partype = current_champ.get("partype", "None")

        allytips = " ".join(champ_details.get("allytips", "None"))
        enemytips = " ".join(champ_details.get("enemytips", "None"))

        c.execute("""INSERT INTO champions
                     (id, name, key, tags, partype, hp, hpperlevel, movespeed, armor, armorperlevel,
                      spellblock, spellblockperlevel, attackrange, attackdamage, attackdamageperlevel,
                      attackspeed, attackspeedperlevel, allytips, enemytips)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (
                      champ_id, current_champ["name"], current_champ["key"], tags, partype,
                      stats["hp"], stats["hpperlevel"], stats["movespeed"],
                      stats["armor"], stats["armorperlevel"], stats["spellblock"], stats["spellblockperlevel"],
                      stats["attackrange"], stats["attackdamage"], stats["attackdamageperlevel"],
                      stats["attackspeed"], stats["attackspeedperlevel"], allytips, enemytips
                  ))

        passive = champ_details.get("passive", {})
        c.execute("""INSERT INTO spells
                         (champion_id, spell_key, name, description, cooldown, cost, range)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (
                      champ_id, 'P', passive.get("name", "Unknown"),
                      _clean_html(passive.get("description", "")),
                      "0", "No cost", "0"
                  ))

        spells = champ_details.get("spells", [])
        spell_keys = ['Q', 'W', 'E', 'R']

        for idx, spell in enumerate(spells):
            key = spell_keys[idx] if idx < 4 else f"Extra_{idx}"

            parsed_desc = _parse_tooltip(
                tooltip=spell.get("tooltip", ""),
                effect_burn=spell.get("effectBurn", []),
                vars_list=spell.get("vars", [])
            )

            parsed_cost = _parse_resource(
                resource_text=spell.get("resource", ""),
                cost_burn=spell.get("costBurn", "0"),
                effect_burn=spell.get("effectBurn", [])
            )

            if not parsed_desc or parsed_desc == "":
                parsed_desc = _clean_html(spell.get("description", ""))

            c.execute("""INSERT INTO spells
                      (champion_id, spell_key, name, description, cooldown, cost, range)
                      VALUES(?, ?, ?, ?, ?, ?, ?)""",
                      (
                          champ_id, key, spell.get("name", ""),
                          parsed_desc,
                          spell.get("cooldownBurn", "0"),
                          parsed_cost,
                          spell.get("rangeBurn", "0")
                      ))
    conn.commit()
    conn.close()

    print("Database filled")


def _clean_item_description(raw_text: str) -> str:
    """Clears the item description of Riot's HTML tags, preserving readability."""
    if not raw_text:
        return ""
    text = re.sub(r'<br\s*/?>', ' ', raw_text)
    text = re.sub(r'<li>', ' * ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def _get_items_list():
    items_response = requests.get(f"{BASE_URL}/item.json").json()
    return items_response["data"]


def prepare_item_for_vectorization(item_data, clean_desc: str) -> str:
    name = item_data.get("name", "")
    tags = ", ".join(item_data.get("tags", []))
    plaintext = item_data.get("plaintext", "")

    vector_text = f"Item Name: {name}. "
    if tags: vector_text += f"Tags: {tags}. "
    if plaintext: vector_text += f"Summary: {plaintext} "
    if clean_desc: vector_text += f"Description: {clean_desc}"

    return vector_text.strip()


def fill_items():
    print("Filling items table...")
    items_list = _get_items_list()

    conn = sqlite3.connect("lol_data.db")

    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    c = conn.cursor()

    total_items = len(items_list)
    processed_count = 0

    for item_id, item_data in items_list.items():
        processed_count += 1
        print(f"\rProcessing items: {processed_count}/{total_items} [{item_id}]{' ' * 10}", end="", flush=True)

        is_purchasable = item_data.get("gold", {}).get("purchasable", False)
        if not is_purchasable:
            continue

        name = item_data.get("name", "")
        plaintext = item_data.get("plaintext", "")
        total_gold = item_data.get("gold", {}).get("total", 0)
        tags = ", ".join(item_data.get("tags", []))
        stats_json = json.dumps(item_data.get("stats", {}))

        clean_desc = _clean_item_description(item_data.get("description", ""))

        c.execute("""INSERT INTO items
                         (id, name, plaintext, description, total_gold, tags, stats_json)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (item_id, name, plaintext, clean_desc, total_gold, tags, stats_json))

        text_to_vectorize = prepare_item_for_vectorization(item_data, clean_desc)
        vector = encoder.encode(text_to_vectorize).tobytes()
        c.execute("""INSERT INTO vec_items
                         (item_id, embedding)
                         VALUES (?, ?)""",
                  (item_id, vector))

    conn.commit()
    conn.close()
    print("Items table filled successfully")

def _get_summoner_spells_list():
    response = requests.get(f"{BASE_URL}/summoner.json").json()
    return response["data"]

def fill_summoner_spells():
    print("Filling summoner spells table...")
    spells_list = _get_summoner_spells_list()

    conn = sqlite3.connect("lol_data.db")
    c = conn.cursor()


    total_spells = len(spells_list)
    for idx, (spell_id, spell_data) in enumerate(spells_list.items(), start=1):
        print(f"\rProcessing summonner spells: {idx}/{total_spells} [{spell_id}]{' ' * 10}", end="", flush=True)

        parsed_desc = _parse_tooltip(
            tooltip=spell_data.get("tooltip", ""),
            effect_burn=spell_data.get("effectBurn", []),
            vars_list=spell_data.get("vars", [])
        )

        if not parsed_desc or parsed_desc == "":
            parsed_desc = _clean_html(spell_data.get("description", ""))

        c.execute("""INSERT INTO summoner_spells 
                     (id, name, key, description, cooldown)
                     VALUES (?, ?, ?, ?, ?)""",
                  (
                      spell_id,
                      spell_data.get("name", ""),
                      int(spell_data.get("key", 0)),
                      parsed_desc,
                      spell_data.get("cooldownBurn", "0")
                  ))

    conn.commit()
    conn.close()
    print("Summoner spells table filled successfully")


# fast function to check functionality of RAG
def find_best_items_for_problem(problem_description: str, limit: int = 3):
    conn = sqlite3.connect("lol_data.db")
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    query_vector = encoder.encode(problem_description).tobytes()

    c = conn.cursor()

    c.execute("""
              SELECT i.name, i.plaintext
              FROM vec_items v
                       JOIN items i ON v.item_id = i.id
              WHERE v.embedding MATCH ?
                AND k = ?
              """, (query_vector, limit))

    results = c.fetchall()
    conn.close()

    return results


if "__main__" == __name__:
    build_database()
    fill_champions()
    fill_items()
    fill_summoner_spells()