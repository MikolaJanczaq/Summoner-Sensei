from Database.connection import get_db_connection
from Database.embeddings import encoder


def find_best_items_for_problem(problem_description: str, limit: int = 3):
    conn = get_db_connection()
    c = conn.cursor()

    query_vector = encoder.encode(problem_description).tobytes()

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


def get_champion_info_for_rag(champion_name: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT tags, partype
                 FROM champions
                 WHERE name = ?""",
              (champion_name,))
    results = c.fetchall()
    conn.close()

    if results:
        return f"{results[0][0]} (Resource: {results[0][1]})"
    return "Unknown champion"
