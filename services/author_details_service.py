from db.connection import get_connection

def create_author_details(author_id, photo_url=None, overview=None, hometown=None, birthday=None, website=None) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO author_details (author_id, photo_url, overview, hometown, birthday, website)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (author_id, photo_url, overview, hometown, birthday, website))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error creating author details: {e}")
        return False

def read_author_details(author_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT author_id, photo_url, overview, hometown, birthday, website
                    FROM author_details
                    WHERE author_id = %s;
                """, (author_id,))
                row = cur.fetchone()
                if row:
                    return {
                        "author_id": row[0],
                        "photo_url": row[1],
                        "overview": row[2],
                        "hometown": row[3],
                        "birthday": row[4],
                        "website": row[5]
                    }
    except Exception as e:
        print(f"Error reading author details: {e}")
        return None

def update_author_details(author_id, photo_url=None, overview=None, hometown=None, birthday=None, website=None) -> bool:
    if all(v is None for v in [photo_url, overview, hometown, birthday, website]):
        print(f"No details require changing.")
        return True
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT photo_url, overview, hometown, birthday, website
                    FROM author_details
                    WHERE author_id = %s;
                """, (author_id,))
                details = cur.fetchone()
                if not details:
                    print(f"No details found for author ID {author_id}")
                    return False

                photo_url = photo_url if photo_url is not None else details[0]
                overview = overview if overview is not None else details[1]
                hometown = hometown if hometown is not None else details[2]
                birthday = birthday if birthday is not None else details[3]
                website = website if website is not None else details[4]

                cur.execute("""
                    UPDATE author_details
                    SET photo_url = %s,
                        overview = %s,
                        hometown = %s,
                        birthday = %s,
                        website = %s,
                    WHERE author_id = %s;
                """, (photo_url, overview, hometown, birthday, website, author_id))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error updating author details: {e}")
        return False

def delete_author_details(author_id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE
                    FROM author_details
                    WHERE author_id = %s;
                """, (author_id,))
                if cur.rowcount == 0:
                    print(f"No details found for author ID {author_id}")
                    return False
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting author details: {e}")
        return False