from services.crud.crud_service import crud

name = "book_discounts"

create = """INSERT INTO book_discounts (book_id, discount_id)
                          VALUES (%s, %s);"""

read_all = """SELECT * FROM book_discounts;"""

read_all_for_book = """SELECT d.id, d.name, d.discount_type, d.value, d.start_date, d.end_date
                         FROM discounts d
                         JOIN book_discounts bd ON d.id = bd.discount_id
                         WHERE bd.book_id = %s
                            AND CURRENT_DATE BETWEEN d.start_date AND d.end_date;"""

read_one = """SELECT * FROM book_discounts
                            WHERE book_id = %s AND discount_id = %s;"""

delete = """DELETE FROM book_discounts
                          WHERE book_id = %s AND discount_id = %s;"""


def add_book_discount(book_id, discount_id) -> bool:
    return crud("create", create, name, (book_id, discount_id))

def read_all_book_discounts():
    return crud("read_all", read_all, name)

def read_all_current_discounts_for_book(book_id):
    crud("read_all", read_all_for_book, name, (book_id,))

def read_book_discount(book_id, discount_id):
    return crud("read_one", read_one, name, (book_id, discount_id))

def delete_book_discount(book_id, discount_id) -> bool:
    return crud("delete", delete, name, (book_id, discount_id))