from db.connection import get_connection

def create_book_details(book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO book_details (book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error creating book details, error {e}!")
        return False

def read_book_details(book_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT overview, publication_date, page_count, length_cm, width_cm, height_cm
                    FROM books
                    WHERE id = %s;
                """, (book_id,))
                row = cur.fetchone()
                if row:
                    return {
                        "overview": row[0],
                        "publication_date": row[1],
                        "page_count": row[2],
                        "length_cm": row[3],
                        "width_cm": row[4],
                        "height_cm": row[5]
                    }
    except Exception as e:
        print(f"Error reading book details for book ID {book_id}, error {e}!")
        return None

def update_book_details(book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT overview, publication_date, page_count, length_cm, width_cm, height_cm
                    FROM book_details
                    WHERE id = %s;
                """, (book_id,))
                book = cur.fetchone()

                if not book:
                    print(f"Book with ID {book_id} not found!")
                    return False

                overview = overview if overview is not None else book[0]
                publication_date = publication_date if publication_date is not None else book[1]
                page_count = page_count if page_count is not None else book[2]
                length_cm = length_cm if length_cm is not None else book[3]
                width_cm = width_cm if width_cm is not None else book[4]
                height_cm = height_cm if height_cm is not None else book[5]

                cur.execute("""
                    UPDATE books
                    SET overview = %s,
                        publication_date = %s,
                        page_count = %s,
                        length_cm = %s,
                        width_cm = %s,
                        height_cm = %s
                    WHERE book_id = %s;
                """, (overview, publication_date, page_count, length_cm, width_cm, height_cm, book_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Couldn't update book details for book ID {book_id}, error {e}!")
        return False

def delete_book_details(book_id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE
                    FROM book_details
                    WHERE id = %s;
                """, (book_id,))
                if cur.rowcount() == 0:
                    print(f"No book details found for book ID {book_id}")
                    return False
                conn.commit()
                return True
    except Exception as e:
        print(f"Error deleting book details for book ID {book_id}, exception {e}!")
        return False