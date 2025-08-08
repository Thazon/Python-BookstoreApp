from gui.main_window import MainWindow
from models.db_model import create_tables
from services.currency_service import update_exchange_rates

if __name__ == '__main__':
    create_tables()
    update_exchange_rates()
    app = MainWindow()
    app.run()