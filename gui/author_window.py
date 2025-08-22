import tkinter as tk
from tkinter import ttk, messagebox
from services.crud.author_service import (
    create_author, read_all_authors, update_author, delete_author
)

class AuthorWindow:
    def __init__(self, master):
        self.tree = None
        self.first_name_entry = None
        self.last_name_entry = None
        self.master = master
        self.master.title("Author Management")
        self.master.geometry("600x400")
        self.create_widgets()
        self.populate_authors()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.master, columns=("id", "first_name", "last_name"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.column("id", width=30)
        self.tree.pack(pady=10, fill=tk.X)

        form = tk.Frame(self.master)
        form.pack()

        tk.Label(form, text="First Name").grid(row=0, column=0)
        self.first_name_entry = tk.Entry(form)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(form, text="Last Name").grid(row=1, column=0)
        self.last_name_entry = tk.Entry(form)
        self.last_name_entry.grid(row=1, column=1)

        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Author", command=self.add_author).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Author", command=self.update_author).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Author", command=self.delete_author).grid(row=0, column=2, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def populate_authors(self):
        self.tree.delete(*self.tree.get_children())
        for author in read_all_authors():
            self.tree.insert("", "end", values=(author[0], author[1], author[2]))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.first_name_entry.delete(0, tk.END)
            self.first_name_entry.insert(0, values[1])
            self.last_name_entry.delete(0, tk.END)
            self.last_name_entry.insert(0, values[2])
    def add_author(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        if create_author(first_name, last_name):
            messagebox.showinfo("Success", "Author added.")
            self.populate_authors()
        else:
            messagebox.showerror("Error", "Failed to add author.")

    def update_author(self):
        selected = self.tree.selection()
        if selected:
            author_id = self.tree.item(selected[0], "values")[0]
            new_first = self.first_name_entry.get()
            new_last = self.last_name_entry.get()
            if update_author(int(author_id), new_first, new_last):
                messagebox.showinfo("Success", "Author updated.")
                self.populate_authors()
            else:
                messagebox.showerror("Error", "Failed to update author.")

    def delete_author(self):
        selected = self.tree.selection()
        if selected:
            author_id = self.tree.item(selected[0], "values")[0]
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this author?")
            if confirm and delete_author(int(author_id)):
                messagebox.showinfo("Success", "Author deleted")
                self.populate_authors()

def open_author_window():
    win = tk.Toplevel()
    AuthorWindow(win)