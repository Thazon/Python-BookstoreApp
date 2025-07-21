from models.db_model import create_tables
from cli.interface import run

if __name__ == '__main__':
    create_tables()
    run()