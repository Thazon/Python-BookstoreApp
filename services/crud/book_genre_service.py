from services.crud.crud_service import crud

name = "book_genres"

create = """INSERT INTO book_genres (book_id, genre_id)
            VALUES (%s, %s);"""

read_all = """SELECT book_id, genre_id
              FROM book_genres;"""

read_by_book = """SELECT genre_id
                  FROM book_genres
                  WHERE book_id = %s;"""

read_by_genre = """SELECT book_id
                   FROM book_genres
                   WHERE genre_id = %s;"""

delete = """DELETE FROM book_genres
            WHERE book_id = %s AND genre_id = %s;"""

def create_book_genre(book_id, genre_id) -> bool:
    return crud("create", create, name, (book_id, genre_id))

def read_all_book_genres():
    return crud("read_all", read_all, name)

def read_genres_for_book(book_id):
    return crud("read_all", read_by_book, name, (book_id,))

def read_books_for_genre(genre_id):
    return crud("read_all", read_by_genre, name, (genre_id,))

def delete_book_genre(book_id, genre_id) -> bool:
    return crud("delete", delete, name, (book_id, genre_id))
