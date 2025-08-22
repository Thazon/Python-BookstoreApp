from services.crud.crud_service import crud

name = "orders"

create = """INSERT INTO orders (customer_id, order_date)
            VALUES (%s, CURRENT_TIMESTAMP)
            RETURNING id;"""

read_all = """SELECT id, customer_id, order_date
              FROM orders;"""

read_one = """SELECT id, customer_id, order_date
              FROM orders
              WHERE id = %s;"""

update_select = """SELECT customer_id
                   FROM orders
                   WHERE id = %s;"""

update = """UPDATE orders
            SET customer_id = %s
            WHERE id = %s;"""

delete = """DELETE FROM orders
            WHERE id = %s;"""

def create_order(customer_id) -> int | None:
    return crud("create_return", create, name, (customer_id,))

def read_all_orders():
    return crud("read_all", read_all, name)

def read_order(order_id):
    return crud("read_one", read_one, name, (order_id,))

def update_order_customer(order_id, customer_id) -> bool:
    return crud("update", update, name, (customer_id, order_id), update_select)

def delete_order(order_id) -> bool:
    return crud("delete", delete, name, (order_id,))
