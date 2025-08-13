from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from services.crud_service import crud

ph = PasswordHasher()

name = "accounts"
name_customers = "customers"

create = """INSERT INTO accounts (username, password)
            VALUES (%s, %s)
            RETURNING id;"""

create_customer = """INSERT INTO customers (account_id, first_name, last_name, email)
                        VALUES (%s, %s, %s, %s);"""

read_one_username ="""SELECT 1
                        FROM accounts
                        WHERE username = %s;"""

read_one_account_username = """SELECT a.id, a.username, c.first_name, c.last_name, c.email
                        FROM accounts a
                        JOIN customers c ON a.id = c.account_id
                        WHERE a.username = %s;"""

read_all = """SELECT a.id, a.username, c.first_name, c.last_name, c.email
                FROM accounts a
                JOIN customers c ON a.id = c.account_id;"""

read_password = """SELECT password
                    FROM accounts
                    WHERE username = %s;"""

update = """UPDATE accounts
            SET is_active = %s
            WHERE id = %s;"""

delete = """DELETE
            FROM accounts
            WHERE id = %s;"""



def create_account(username, password, first_name, last_name, email) -> bool:
    while is_username_taken(username):
        print("Username already exists. Pick a different username.")
        username = input("New username: ")

    hashed_password = ph.hash(password)
    account_id = crud("read_one", create, name, (username, hashed_password))

    if not account_id:
        return False
    account_id = account_id[0]

    return crud("create", create_customer, name_customers, (account_id, first_name, last_name, email))

def is_username_taken(username) -> bool:
    return crud("read_one", read_one_username, "username_check", (username,)) is not None

def read_account_by_username(username):
    return crud("read_one", read_one_account_username, name, (username,))

def read_all_accounts():
    return crud("read_all", read_all, name)

def update_active_account(account_id, state) -> bool:
    return crud("update", update, name, (state, account_id))

def delete_account(account_id) -> bool:
    return crud("delete", delete, name, (account_id,))

def verify_login(username, password) -> bool:
    result = crud("read_one", read_password, name, (username,))
    if not result:
        return False
    stored_password = result[0]
    try:
        ph.verify(stored_password, password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Error verifying login: {e}")
        return False