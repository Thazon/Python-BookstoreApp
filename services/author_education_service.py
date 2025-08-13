from services.crud_service import crud

name = "author_education"

create = """INSERT INTO author_education (author_id, degree, institution, graduation_year)
            VALUES (%s, %s, %s, %s, %s);"""

read_all = """SELECT id, author_id, degree, institution, graduation_year
                FROM author_education
                WHERE author_id = %s
                ORDER BY graduation_year;"""

update_select = """SELECT degree, institution, graduation_year
                    FROM author_education
                    WHERE id = %s;"""

update = """UPDATE author_education
            SET degree = %s,
                institution = %s,
                graduation_year = %s,
            WHERE id = %s;"""

delete = """DELETE
            FROM author_education
            WHERE id = %s;"""

def create_author_education(author_id, degree, institution, graduation_year=None) -> bool:
    return crud("create", create, name, (author_id, degree, institution, graduation_year))

def read_author_education(author_id):
    return crud("read_all", read_all, name, (author_id,))

def update_author_education(author_id, degree=None, institution=None, graduation_year=None) -> bool:
    return crud("update", update, name, (degree, institution, graduation_year, author_id), update_select)

def delete_author_education(author_id) -> bool:
    return crud("delete", delete, name, (author_id,))