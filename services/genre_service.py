from services.crud_service import crud

name = "genres"

create = """INSERT INTO genres (name)
            VALUES (%s);"""

read_one = """SELECT name
                FROM genres
                WHERE id = %s;"""

read_all = """SELECT id, name
                FROM genres;"""

update_select = """SELECT name
                    FROM genres
                    WHERE id = %s;"""

update = """UPDATE genres
            SET name = %s
            WHERE genre_id = %s;"""

delete = """DELETE
            FROM genres
            WHERE id = %s;"""

def create_genre(genre_name):
    return crud("create", create, name, (genre_name,))

def read_genre(genre_id):
    return crud("read_one", read_one, name, (genre_id,))

def read_all_genres():
    return crud("read_all", read_all, name)

def update_genre(genre_id, genre_name) -> bool:
    return crud("update", update, name, (genre_name, genre_id), update_select)

def delete_genre(genre_id) -> bool:
    return crud("delete", delete, name, (genre_id,))