from services.crud_service import crud

name = "authors"

create = """INSERT INTO authors (first_name, last_name)
            VALUES (%s, %s);"""

read_all = """SELECT id, first_name, last_name
            FROM authors;"""

read_one = """SELECT id, first_name, last_name
            FROM authors
            WHERE id = %s;"""

update_select = """SELECT first_name, last_name
                FROM authors
                WHERE id = %s;"""

update = """UPDATE authors
            SET first_name = %s, last_name = %s
            WHERE id = %s;"""

delete = """DELETE
            FROM authors
            WHERE id = %s;"""

def create_author(first_name, last_name) -> bool:
    return crud("create", create, name, (first_name, last_name))

def read_all_authors():
    return crud("read_all", read_all, name)

def read_author(author_id):
    return crud("read_one", read_one, name, (author_id,))

def update_author(first_name, last_name, author_id) -> bool:
    return crud("update", update, name, (first_name, last_name, author_id), update_select)

def delete_author(author_id) -> bool:
    return crud("delete", delete, name, (author_id,))