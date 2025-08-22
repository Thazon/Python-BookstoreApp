from services.crud.crud_service import crud

name = "book_details"

create = """INSERT INTO book_details (book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm)
            VALUES (%s, %s, %s, %s, %s, %s, %s);"""

read_one = """SELECT overview, publication_date, page_count, length_cm, width_cm, height_cm
                FROM books
                WHERE id = %s;"""

update_select = """SELECT overview, publication_date, page_count, length_cm, width_cm, height_cm
                    FROM book_details
                    WHERE id = %s;"""

update = """UPDATE books
            SET overview = %s,
                publication_date = %s,
                page_count = %s,
                length_cm = %s,
                width_cm = %s,
                height_cm = %s
            WHERE book_id = %s;"""

delete = """DELETE
            FROM book_details
            WHERE id = %s;"""

def create_book_details(book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm):
    return crud("create", create, name, (book_id, overview, publication_date, page_count,
                                         length_cm, width_cm, height_cm))

def read_book_details(book_id):
    return crud("read_one", read_one, name, (book_id,))

def update_book_details(book_id, overview, publication_date, page_count, length_cm, width_cm, height_cm) -> bool:
    return crud("update", update, name, (overview, publication_date, page_count, length_cm,
                                         width_cm, height_cm, book_id), update_select)

def delete_book_details(book_id) -> bool:
    return crud("delete", delete, name, (book_id,))