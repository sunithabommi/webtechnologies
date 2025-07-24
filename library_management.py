import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'library.db'

# --- DATABASE FUNCTIONS ---

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantity INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issued (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            borrower_id INTEGER,
            issue_date TEXT,
            due_date TEXT,
            returned INTEGER DEFAULT 0,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(borrower_id) REFERENCES borrowers(id)
        )
    ''')
    conn.commit()
    return conn

def add_book(title, author, isbn, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, isbn, quantity) VALUES (?, ?, ?, ?)',
                   (title, author, isbn, quantity))
    conn.commit()
    conn.close()

def get_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_borrower(name, contact):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO borrowers (name, contact) VALUES (?, ?)', (name, contact))
    conn.commit()
    conn.close()

def get_borrowers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM borrowers')
    rows = cursor.fetchall()
    conn.close()
    return rows

def issue_book(book_id, borrower_id, issue_date, due_date):
    conn = connect_db()
    cursor = conn.cursor()
    # Check book quantity
    cursor.execute('SELECT quantity FROM books WHERE id=?', (book_id,))
    quantity = cursor.fetchone()[0]
    if quantity <= 0:
        conn.close()
        return False, "Book not available for issue"
    # Insert into issued
    cursor.execute('INSERT INTO issued (book_id, borrower_id, issue_date, due_date) VALUES (?, ?, ?, ?)',
                   (book_id, borrower_id, issue_date, due_date))
    # Reduce book quantity by 1
    cursor.execute('UPDATE books SET quantity = quantity - 1 WHERE id=?', (book_id,))
    conn.commit()
    conn.close()
    return True, "Book issued successfully"

def get_issued_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT issued.id, books.title, borrowers.name, issued.issue_date, issued.due_date, issued.returned
        FROM issued
        JOIN books ON issued.book_id = books.id
        JOIN borrowers ON issued.borrower_id = borrowers.id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def return_book(issue_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Mark issued record as returned
    cursor.execute('UPDATE issued SET returned=1 WHERE id=?', (issue_id,))
    # Get book id to increase quantity
    cursor.execute('SELECT book_id FROM issued WHERE id=?', (issue_id,))
    book_id = cursor.fetchone()[0]
    cursor.execute('UPDATE books SET quantity = quantity + 1 WHERE id=?', (book_id,))
    conn.commit()
    conn.close()

# --- GUI CLASSES ---

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Book Management System")
        self.geometry("900x600")

        tabControl = ttk.Notebook(self)
        self.book_tab = BookTab(tabControl)
        self.borrower_tab = BorrowerTab(tabControl)
        self.issue_tab = IssueTab(tabControl)

        tabControl.add(self.book_tab, text="Books")
        tabControl.add(self.borrower_tab, text="Borrowers")
        tabControl.add(self.issue_tab, text="Issue/Return")
        tabControl.pack(expand=1, fill="both")

class BookTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Form
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(form, text="Quantity:").grid(row=3, column=0, padx=5, pady=5)

        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.quantity_var = tk.IntVar()

        tk.Entry(form, textvariable=self.title_var).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.author_var).grid(row=1, column=1)
        tk.Entry(form, textvariable=self.isbn_var).grid(row=2, column=1)
        tk.Entry(form, textvariable=self.quantity_var).grid(row=3, column=1)

        tk.Button(form, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Treeview for books
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "ISBN", "Quantity"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.pack(expand=True, fill="both", pady=10)

        self.load_books()

    def add_book(self):
        title = self.title_var.get()
        author = self.author_var.get()
        isbn = self.isbn_var.get()
        quantity = self.quantity_var.get()

        if not title or not author or not isbn or quantity <= 0:
            messagebox.showerror("Error", "Please fill all fields with valid data.")
            return

        try:
            add_book(title, author, isbn, quantity)
            messagebox.showinfo("Success", "Book added successfully.")
            self.clear_fields()
            self.load_books()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def load_books(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in get_books():
            self.tree.insert("", "end", values=row)

    def clear_fields(self):
        self.title_var.set("")
        self.author_var.set("")
        self.isbn_var.set("")
        self.quantity_var.set(0)

class BorrowerTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Contact:").grid(row=1, column=0, padx=5, pady=5)

        self.name_var = tk.StringVar()
        self.contact_var = tk.StringVar()

        tk.Entry(form, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(form, textvariable=self.contact_var).grid(row=1, column=1)

        tk.Button(form, text="Add Borrower", command=self.add_borrower).grid(row=2, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Contact"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.pack(expand=True, fill="both", pady=10)

        self.load_borrowers()

    def add_borrower(self):
        name = self.name_var.get()
        contact = self.contact_var.get()

        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        try:
            add_borrower(name, contact)
            messagebox.showinfo("Success", "Borrower added successfully.")
            self.clear_fields()
            self.load_borrowers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add borrower: {e}")

    def load_borrowers(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in get_borrowers():
            self.tree.insert("", "end", values=row)

    def clear_fields(self):
        self.name_var.set("")
        self.contact_var.set("")

class IssueTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Issue book frame
        issue_frame = tk.LabelFrame(self, text="Issue Book")
        issue_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(issue_frame, text="Select Book:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(issue_frame, text="Select Borrower:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(issue_frame, text="Due Days (from today):").grid(row=2, column=0, padx=5, pady=5)

        self.book_var = tk.StringVar()
        self.borrower_var = tk.StringVar()
        self.due_days_var = tk.IntVar(value=7)

        self.book_combo = ttk.Combobox(issue_frame, textvariable=self.book_var, state="readonly", width=50)
        self.borrower_combo = ttk.Combobox(issue_frame, textvariable=self.borrower_var, state="readonly", width=50)
        self.book_combo.grid(row=0, column=1, padx=5, pady=5)
        self.borrower_combo.grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(issue_frame, textvariable=self.due_days_var, width=5).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(issue_frame, text="Issue Book", command=self.issue_book).grid(row=3, column=0, columnspan=2, pady=10)

        # Issued books treeview
        issued_frame = tk.LabelFrame(self, text="Issued Books")
        issued_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(issued_frame, columns=("ID", "Book Title", "Borrower", "Issue Date", "Due Date", "Returned"), show="headings")
        for col in ("ID", "Book Title", "Borrower", "Issue Date", "Due Date", "Returned"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(issued_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Return book button
        tk.Button(self, text="Return Selected Book", command=self.return_book).pack(pady=10)

        self.load_books_and_borrowers()
        self.load_issued_books()

    def load_books_and_borrowers(self):
        books = get_books()
        book_list = [f"{b[0]}: {b[1]} (Qty: {b[4]})" for b in books]
        self.book_combo['values'] = book_list

        borrowers = get_borrowers()
        borrower_list = [f"{b[0]}: {b[1]}" for b in borrowers]
        self.borrower_combo['values'] = borrower_list

    def issue_book(self):
        if not self.book_var.get() or not self.borrower_var.get():
            messagebox.showerror("Error", "Please select a book and borrower.")
            return

        try:
            book_id = int(self.book_var.get().split(":")[0])
            borrower_id = int(self.borrower_var.get().split(":")[0])
            issue_date = datetime.now().strftime("%Y-%m-%d")
            due_days = self.due_days_var.get()
            if due_days <= 0:
                messagebox.showerror("Error", "Due days must be positive.")
                return
            due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")

            success, msg = issue_book(book_id, borrower_id, issue_date, due_date)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_books_and_borrowers()
                self.load_issued_books()
            else:
                messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {e}")

    def load_issued_books(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in get_issued_books():
            returned_str = "Yes" if row[5] else "No"
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], returned_str))

    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an issued book to return.")
            return
        issue_id = self.tree.item(selected[0])['values'][0]
        # Check if already returned
        if self.tree.item(selected[0])['values'][5] == "Yes":
            messagebox.showinfo("Info", "This book is already returned.")
            return
        return_book(issue_id)
        messagebox.showinfo("Success", "Book returned successfully.")
        self.load_books_and_borrowers()
        self.load_issued_books()

# --- RUN APP ---
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
