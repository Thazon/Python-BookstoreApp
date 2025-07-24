from gui.main_window import MainWindow
from models.db_model import create_tables

if __name__ == '__main__':
    create_tables()
    app = MainWindow()
    app.run()