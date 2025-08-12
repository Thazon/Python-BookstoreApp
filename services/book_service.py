from db.connection import get_connection

def create_book(cover_image_url, title, author_id, publisher, isbn, price, book_format, stock=0):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO books (cover_image_url, title, author_id, publisher, isbn, price, book_format, stock)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (cover_image_url, title, author_id, publisher, isbn, price, book_format, stock))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error creating book, error {e}!")
        return False

def read_book(book_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT cover_image_url, title, author_id, publisher, isbn, price, book_format, stock
                    FROM books
                    WHERE id = %s;
                """, (book_id,))
                row = cur.fetchone()
                if row:
                    return {
                        "cover_image_url": row[0],
                        "title": row[1],
                        "author_id": row[2],
                        "publisher": row[3],
                        "ISBN": row[4],
                        "price": row[5],
                        "book_format": row[6],
                        "stock": row[7]
                    }
    except Exception as e:
        print(f"Error reading book {book_id}, error {e}!")
        return None

def read_all_books():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, cover_image_url, title, author_id, publisher, isbn, price, book_format, stock
                    FROM books;
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Error reading all books, error {e}!")
        return None

def update_book(book_id, cover_image_url, title, author_id, publisher, isbn, price, book_format, stock) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT cover_image_url, title, author_id, publisher, isbn, price, book_format, stock
                    FROM books
                    WHERE id = %s;
                """, (book_id,))
                book = cur.fetchone()

                if not book:
                    print(f"Book with ID {book_id} not found!")
                    return False

                cover_image_url = cover_image_url if cover_image_url is not None else book[0]
                title = title if title is not None else book[1]
                author_id = author_id if author_id is not None else book[2]
                publisher = publisher if publisher is not None else book[3]
                isbn = isbn if isbn is not None else book[4]
                price = price if price is not None else book[5]
                book_format = book_format if book_format is not None else book[6]
                stock = stock if stock is not None else book[7]

                cur.execute("""
                    UPDATE books
                    SET cover_image_url = %s,
                        title = %s,
                        author_id = %s,
                        publisher = %s,
                        isbn = %s,
                        price = %s,
                        book_format = %s,
                        stock = %s
                    WHERE book_id = %s;
                """, (cover_image_url, title, author_id, publisher, isbn, price, book_format, stock, book_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Couldn't update book {book_id}, error {e}!")
        return False

def delete_book(book_id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE
                    FROM books
                    WHERE id = %s;
                """, (book_id,))
                if cur.rowcount() == 0:
                    print(f"No book found with id {book_id}")
                    return False
                conn.commit()
                return True
    except Exception as e:
        print(f"Error deleting book {book_id}, exception {e}!")
        return False