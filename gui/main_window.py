import tkinter as tk
from gui.author_window import AuthorWindow

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bookstore Management System")
        self.root.geometry("450x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Welcome to the Bookstore Management System", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.root, text="Manage Authors", width=20, command=self.open_author_window).pack(pady=10)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack(pady=10)

    def open_author_window(self):
        top = tk.Toplevel(self.root)
        AuthorWindow(top)

    def run(self):
        self.root.mainloop()