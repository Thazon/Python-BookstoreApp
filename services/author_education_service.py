from db.connection import get_connection

def create_author_education(author_id, degree, institution, graduation_year=None) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO author_education (author_id, degree, institution, graduation_year)
                    VALUES (%s, %s, %s, %s, %s);
                """, (author_id, degree, institution, graduation_year))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error creating author education: {e}")
        return False

def read_author_education(author_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, author_id, degree, institution, graduation_year
                    FROM author_education
                    WHERE author_id = %s
                    ORDER BY graduation_year;
                """, (author_id,))
                rows = cur.fetchall()
                return [
                    {
                        "id": r[0],
                        "author_id": r[1],
                        "degree": r[2],
                        "institution": r[3],
                        "graduation_year": r[4]
                    }
                    for r in rows
                ]
    except Exception as e:
        print(f"Error reading author education: {e}")
        return None

def update_author_education(id, degree=None, institution=None, graduation_year=None) -> bool:
    if all(v is None for v in[degree, institution, graduation_year]):
        print("No fields to update.")
        return True
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT degree, institution, graduation_year
                    FROM author_education
                    WHERE id = %s;
                """, (id,))
                record = cur.fetchone()
                if not record:
                    print(f"No education record found with ID {id}!")
                    return False

                degree = degree if degree is not None else record[0]
                institution = institution if institution is not None else record[1]
                graduation_year = graduation_year if graduation_year is not None else record[2]

                cur.execute("""
                    UPDATE author_education
                    SET degree = %s,
                        institution = %s,
                        graduation_year = %s,
                    WHERE id = %s;
                """, (degree, institution, graduation_year, id))
                conn.commit()
            return True
    except Exception as e:
        print(f"Error updating author education: {e}")
        return False

def delete_author_education(id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE
                    FROM author_education
                    WHERE id = %s;
                """, (id,))
                if cur.rowcount == 0:
                    print(f"No education record found with ID {id}!")
                    return False
                conn.commit()
            return True
    except Exception as e:
        print (f"Error deleting author education: {e}")
        return False