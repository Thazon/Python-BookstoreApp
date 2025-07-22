from models.db_model import create_tables
from cli.interface import run
from services.account_service import create_account, verify_login

if __name__ == '__main__':
    create_tables()
    create_account(
        username="john_doe",
        password="SecurePass123!",
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )
    if verify_login("john_doe", "SecurePass123!"):
        print("Yes")
    else: print("No")
    run()