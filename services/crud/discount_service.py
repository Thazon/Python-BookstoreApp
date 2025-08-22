from services.crud.crud_service import crud

name = "discounts"

create = """INSERT INTO discounts (name, discount_type, value, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;"""

read_all = """SELECT id, name, discount_type, value, start_date, end_date
              FROM discounts;"""

read_one = """SELECT id, name, discount_type, value, start_date, end_date
              FROM discounts
              WHERE id = %s;"""

update_select = """SELECT name, discount_type, value, start_date, end_date
                   FROM discounts
                   WHERE id = %s;"""

update = """UPDATE discounts
            SET name = %s,
                discount_type = %s,
                value = %s,
                start_date = %s,
                end_date = %s
            WHERE id = %s;"""

delete = """DELETE FROM discounts
            WHERE id = %s;"""

def create_discount(name, discount_type, value, start_date=None, end_date=None) -> int | None:
    return crud("create_return", create, name, (name, discount_type, value, start_date, end_date))

def read_all_discounts():
    return crud("read_all", read_all, name)

def read_discount(discount_id):
    return crud("read_one", read_one, name, (discount_id,))

def update_discount(discount_id, name=None, discount_type=None, value=None, start_date=None, end_date=None) -> bool:
    return crud("update", update, name, (name, discount_type, value, start_date, end_date, discount_id), update_select)

def delete_discount(discount_id) -> bool:
    return crud("delete", delete, name, (discount_id,))
