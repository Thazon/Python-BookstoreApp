from services.crud.crud_service import crud

name = "order_items"

create = """INSERT INTO order_items (order_id, book_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            RETURNING id;"""

read_all = """SELECT id, order_id, book_id, quantity, unit_price
              FROM order_items;"""

read_one = """SELECT id, order_id, book_id, quantity, unit_price
              FROM order_items
              WHERE id = %s;"""

read_by_order = """SELECT id, order_id, book_id, quantity, unit_price
                   FROM order_items
                   WHERE order_id = %s;"""

update_select = """SELECT order_id, book_id, quantity, unit_price
                   FROM order_items
                   WHERE id = %s;"""

update = """UPDATE order_items
            SET order_id = %s,
                book_id = %s,
                quantity = %s,
                unit_price = %s
            WHERE id = %s;"""

delete = """DELETE FROM order_items
            WHERE id = %s;"""

# CRUD functions
def create_order_item(order_id, book_id, quantity, unit_price) -> int | None:
    return crud("create_return", create, name, (order_id, book_id, quantity, unit_price))

def read_all_order_items():
    return crud("read_all", read_all, name)

def read_order_item(item_id):
    return crud("read_one", read_one, name, (item_id,))

def read_items_by_order(order_id):
    return crud("read_all", read_by_order, name, (order_id,))

def update_order_item(item_id, order_id=None, book_id=None, quantity=None, unit_price=None) -> bool:
    return crud("update", update, name, (order_id, book_id, quantity, unit_price, item_id), update_select)

def delete_order_item(item_id) -> bool:
    return crud("delete", delete, name, (item_id,))
