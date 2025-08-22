from services.crud.crud_service import crud

name = "genre_discounts"

create = """INSERT INTO genre_discounts (genre_id, discount_id)
                           VALUES (%s, %s);"""

read_all = """SELECT * FROM genre_discounts;"""

read_all_for_book = """SELECT d.id, d.name, d.discount_type, d.value, d.start_date, d.end_date
                          FROM discounts d
                          JOIN genre_discounts gd ON d.id = gd.discount_id
                          JOIN book_genres bg ON gd.genre_id = bg.genre_id
                          WHERE bg.book_id = %s
                            AND CURRENT_DATE BETWEEN d.start_date AND d.end_date;"""

read_one = """SELECT * FROM genre_discounts
                             WHERE genre_id = %s AND discount_id = %s;"""

delete = """DELETE FROM genre_discounts
                           WHERE genre_id = %s AND discount_id = %s;"""


def add_genre_discount(genre_id, discount_id) -> bool:
    return crud("create", create, name, (genre_id, discount_id))

def read_all_genre_discounts():
    return crud("read_all", read_all, name)

def read_all_current_genre_book_discounts(book_id):
    crud("read_all", read_all_for_book, "discounts", (book_id,))

def read_genre_discount(genre_id, discount_id):
    return crud("read_one", read_one, name, (genre_id, discount_id))

def delete_genre_discount(genre_id, discount_id) -> bool:
    return crud("delete", delete, name, (genre_id, discount_id))