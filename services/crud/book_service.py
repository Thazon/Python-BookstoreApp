from services.crud.crud_service import crud

name = "books"

create = """INSERT INTO books (cover_image_url, title, author_id, publisher, isbn, price, book_format, stock)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

read_one = """SELECT cover_image_url, title, author_id, publisher, isbn, price, book_format, stock
                FROM books
                WHERE id = %s;"""

read_book_price = """SELECT price, id, author_id FROM books WHERE id = %s;"""

read_all = """SELECT id, cover_image_url, title, author_id, publisher, isbn, price, book_format, stock
                FROM books;"""

update_select = """SELECT cover_image_url, title, author_id, publisher, isbn, price, book_format, stock
                    FROM books
                    WHERE id = %s;"""

update = """UPDATE books
            SET cover_image_url = %s,
                title = %s,
                author_id = %s,
                publisher = %s,
                isbn = %s,
                price = %s,
                book_format = %s,
                stock = %s
            WHERE book_id = %s;"""

delete = """DELETE
            FROM books
            WHERE id = %s;"""

def create_book(cover_image_url, title, author_id, publisher, isbn, price, book_format, stock=0):
    return crud("create", create, name, (cover_image_url, title, author_id, publisher, isbn,
                                         price, book_format, stock))

def read_book(book_id):
    return crud("read_one", read_one, name, (book_id,))

def read_price_book(book_id):
    return crud("read_one", read_book_price, name, (book_id,))

def read_all_books():
    return crud("read_all", read_all, name)

def update_book(book_id, cover_image_url, title, author_id, publisher, isbn, price, book_format, stock) -> bool:
    return crud("update", update, name, (cover_image_url, title, author_id, publisher, isbn,
                                         price, book_format, stock, book_id), update_select)

def delete_book(book_id) -> bool:
    return crud("delete", delete, name, (book_id,))