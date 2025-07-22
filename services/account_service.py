import psycopg2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from db.connection import get_connection

ph = PasswordHasher()

def create_account(username, password, first_name, last_name, email) -> bool:
    while is_username_taken(username):
        print("Username already exists. Pick a different username.")
        username = input("New username: ")
    try:
        hashed_password = ph.hash(password)

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO accounts (username, password)
                    VALUES(%s, %s)
                    RETURNING id
                """, (username, hashed_password))

                account_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO customers (account_id, first_name, last_name, email)
                    VALUES (%s, %s, %s, %s)
                """, (account_id, first_name, last_name, email))
                conn.commit()
                return True
    except psycopg2.IntegrityError as e:
        print(f"Integrity error: {e}")
    except Exception as e:
        print(f"Error creating account: {e}")

def is_username_taken(username) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM accounts WHERE username = %s", (username,))
                return cur.fetchone() is not None
    except Exception as e:
        print(f"Error checking username: {e}")
        return True #If an error occurs, it's better to assume the username is taken than to potentially allow a
                    #duplicate username.

def update_active_account(id: int, state: bool) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE accounts
                    SET is_active = %s
                    WHERE id = %s
                """, (state, id))

                if cur.rowcount == 0:
                    print(f"No account found with ID {id}")
                    return False
                conn.commit()
                return True
    except Exception as e:
        print(f"Error updating account status: {e}")
        return False

def read_account_by_username(username):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT a.id, a.username, c.first_name, c.last_name, c.email
                    FROM accounts a
                    JOIN customers c ON a.id = c.account_id
                    WHERE a.username = %s
                """, (username,))
                return cur.fetchone()
    except Exception as e:
        print(f"Error reading account: {e}")
    return None

def read_all_accounts():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT a.id, a.username, c.first_name, c.last_name, c.email
                    FROM accounts a
                    JOIN customers c ON a.id = c.account_id
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Error reading all accounts: {e}")

def delete_account(account_id) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM accounts WHERE id = %s
                """, (account_id,))
                conn.commit()
                return True
    except Exception as e:
        print(f"Error deleting account: {e}")
        return False

def verify_login(username, password) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT password FROM accounts WHERE username = %s
                """, (username,))
                result = cur.fetchone()
                if result is None:
                    return False
                stored_password = result[0]
                ph.verify(stored_password, password)
                return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Error verifying login: {e}")
        return False