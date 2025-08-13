from services.crud_service import crud

name = "author_details"

create = """INSERT INTO author_details (author_id, photo_url, overview, hometown, birthday, website)
            VALUES (%s, %s, %s, %s, %s, %s);"""

read_one = """SELECT author_id, photo_url, overview, hometown, birthday, website
                FROM author_details
                WHERE author_id = %s;"""

update_select = """SELECT photo_url, overview, hometown, birthday, website
                    FROM author_details
                    WHERE author_id = %s;"""

update = """UPDATE author_details
            SET photo_url = %s,
                overview = %s,
                hometown = %s,
                birthday = %s,
                website = %s,
            WHERE author_id = %s;"""

delete = """DELETE
            FROM author_details
            WHERE author_id = %s;"""

def create_author_details(author_id, photo_url=None, overview=None, hometown=None, birthday=None, website=None) -> bool:
    return crud("create", create, name, (author_id, photo_url, overview, hometown, birthday, website))

def read_author_details(author_id):
    return crud("read_one", read_one, name, (author_id,))

def update_author_details(author_id, photo_url=None, overview=None, hometown=None, birthday=None, website=None) -> bool:
    return crud("update", update, name, (photo_url, overview, hometown, birthday, website, author_id), update_select)

def delete_author_details(author_id) -> bool:
    return crud("delete", delete, name, (author_id,))