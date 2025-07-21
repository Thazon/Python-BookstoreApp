from db.connection import get_connection


def create_author(first_name, last_name) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO authors (first_name, last_name)
                    VALUES (%s, %s)
                """, (first_name, last_name))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error creating author: {e}")
        return False

def read_all_authors():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM authors")
            return cur.fetchall()

def read_author_id(author_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, first_name, last_name FROM authors WHERE id = %s", (author_id,))
            return cur.fetchone()

def update_author(id, first_name, last_name) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT first_name, last_name FROM authors WHERE id = %s", (id,))
                author = cur.fetchone()

                if not author:
                    print(f"No author found with ID = {id}.")
                    return False

                current_first_name, current_last_name = author

                final_first_name = first_name.strip() or current_first_name
                final_last_name = last_name.strip() or current_last_name

                cur.execute("""
                    UPDATE authors
                    SET first_name = %s, last_name = %s
                    WHERE id = %s
                """, (final_first_name, final_last_name, id))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating author: {e}")
        return False


def delete_author(id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM authors WHERE id = %s", (id,))
                if cur.fetchone() is None:
                    print(f"No author found with ID {id}.")
                    return False

                cur.execute("DELETE FROM authors WHERE id = %s", (id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting author: {e}")
        return False