import json
import sqlite3

from Database.connection import get_db_connection
from Database.embeddings import encoder
from Database.parsers import clean_html, parse_tooltip, parse_resource, clean_item_description, \
    prepare_item_for_vectorization
from Database.riot_api import get_champions_list, get_champion_details, get_items_list, get_summoner_spells_list


def build_database():
    conn = get_db_connection()
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


def fill_champions():
    print("Filling champions table...")
    champions_list = get_champions_list()
    total_champs = len(champions_list)
    conn = get_db_connection()
    c = conn.cursor()

    for champ_num, champ_id in enumerate(champions_list.keys(), start=1):
        print(f"\rProcessing champs: {champ_num}/{total_champs} [{champ_id}]{' ' * 10}", end="", flush=True)
        current_champ = champions_list[champ_id]
        champ_details = get_champion_details(champ_id)

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
                      clean_html(passive.get("description", "")),
                      "0", "No cost", "0"
                  ))

        spells = champ_details.get("spells", [])
        spell_keys = ['Q', 'W', 'E', 'R']

        for idx, spell in enumerate(spells):
            key = spell_keys[idx] if idx < 4 else f"Extra_{idx}"

            parsed_desc = parse_tooltip(
                tooltip=spell.get("tooltip", ""),
                effect_burn=spell.get("effectBurn", []),
                vars_list=spell.get("vars", [])
            )

            parsed_cost = parse_resource(
                resource_text=spell.get("resource", ""),
                cost_burn=spell.get("costBurn", "0"),
                effect_burn=spell.get("effectBurn", [])
            )

            if not parsed_desc or parsed_desc == "":
                parsed_desc = clean_html(spell.get("description", ""))

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


def fill_items():
    print("Filling items table...")
    items_list = get_items_list()

    conn = get_db_connection()
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

        clean_desc = clean_item_description(item_data.get("description", ""))

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


def fill_summoner_spells():
    print("Filling summoner spells table...")
    spells_list = get_summoner_spells_list()

    conn = get_db_connection()
    c = conn.cursor()


    total_spells = len(spells_list)
    for idx, (spell_id, spell_data) in enumerate(spells_list.items(), start=1):
        print(f"\rProcessing summonner spells: {idx}/{total_spells} [{spell_id}]{' ' * 10}", end="", flush=True)

        parsed_desc = parse_tooltip(
            tooltip=spell_data.get("tooltip", ""),
            effect_burn=spell_data.get("effectBurn", []),
            vars_list=spell_data.get("vars", [])
        )

        if not parsed_desc or parsed_desc == "":
            parsed_desc = clean_html(spell_data.get("description", ""))

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


def initialize_data():
    build_database()
    fill_champions()
    fill_items()
    fill_summoner_spells()


if "__main__" == __name__:
    initialize_data()