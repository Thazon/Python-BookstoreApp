from db.connection import get_connection

def create_genre(name):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO genres (name)
                    VALUES (%s);
                """, (name,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error creating genre, exception {e}!")
        return False

def read_genre(genre_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name
                    FROM genres
                    WHERE id = %s;
                """, (genre_id,))
                return cur.fetchone()
    except Exception as e:
        print(f"Error reading genre {genre_id}, {e}!")
        return None

def read_all_genres():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name
                    FROM genres;
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Error reading all genres, exception {e}!")
        return None

def update_genre(genre_id, name) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name
                    FROM genres
                    WHERE id = %s;
                """, (genre_id,))
                genre = cur.fetchone()

                if not genre:
                    print(f"Genre with ID {genre_id} not found!")
                    return False

                if name is None:
                    print(f"No new genre name given.")
                    return False

                if name == genre:
                    print(f"No genre name change necessary.")
                    return False

                cur.execute("""
                    UPDATE genres
                    SET name = %s
                    WHERE genre_id = %s;
                """, (name, genre_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Couldn't update genre {genre_id}, exception {e}!")
        return False

def delete_genre(genre_id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE
                    FROM genres
                    WHERE id = %s;
                """, (genre_id,))
                if cur.rowcount() == 0:
                    print(f"No genre found with id {genre_id}")
                    return False
                conn.commit()
                return True
    except Exception as e:
        print(f"Error deleting genre with id {genre_id}, exception {e}!")
        return False