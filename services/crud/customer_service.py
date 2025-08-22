from services.crud.crud_service import crud

name = "customers"

create = """INSERT INTO customers (account_id, first_name, last_name, email)
            VALUES (%s, %s, %s, %s);"""

read_all = """SELECT id, account_id, first_name, last_name, email
              FROM customers;"""

read_one = """SELECT id, account_id, first_name, last_name, email
              FROM customers
              WHERE id = %s;"""

update_select = """SELECT account_id, first_name, last_name, email
                   FROM customers
                   WHERE id = %s;"""

update = """UPDATE customers
            SET account_id = %s, first_name = %s, last_name = %s, email = %s
            WHERE id = %s;"""

delete = """DELETE FROM customers
            WHERE id = %s;"""

def create_customer(account_id, first_name, last_name, email) -> bool:
    return crud("create", create, name, (account_id, first_name, last_name, email))

def read_all_customers():
    return crud("read_all", read_all, name)

def read_customer(customer_id):
    return crud("read_one", read_one, name, (customer_id,))

def update_customer(account_id, first_name, last_name, email, customer_id) -> bool:
    return crud("update", update, name, (account_id, first_name, last_name, email, customer_id), update_select)

def delete_customer(customer_id) -> bool:
    return crud("delete", delete, name, (customer_id,))
