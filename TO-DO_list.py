import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.is_dark = False
        self.task_file = "tasks.txt"

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        self.header = tk.Label(self.root, text="To-Do List", font=("Helvetica", 16, "bold"))
        self.header.pack(pady=10)

        self.task_entry = tk.Entry(self.root, font=("Helvetica", 12), width=25)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Task", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(self.root, font=("Helvetica", 12), width=30, height=10)
        self.task_listbox.pack(pady=10)

        self.done_button = tk.Button(self.root, text="Mark as Done", width=20, command=self.mark_done)
        self.done_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Tasks", width=20, command=self.save_tasks)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load Tasks", width=20, command=self.load_tasks)
        self.load_button.pack(pady=5)

        self.theme_button = tk.Button(self.root, text="Toggle Dark Mode", width=20, command=self.toggle_theme)
        self.theme_button.pack(pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_listbox.delete(selected[0])
        else:
            messagebox.showinfo("Delete Task", "Please select a task to delete.")

    def mark_done(self):
        selected = self.task_listbox.curselection()
        if selected:
            task = self.task_listbox.get(selected)
            if not task.startswith("✔️ "):
                self.task_listbox.delete(selected)
                self.task_listbox.insert(selected, "✔️ " + task)
        else:
            messagebox.showinfo("Mark as Done", "Please select a task.")

    def save_tasks(self):
        try:
            with open(self.task_file, "w") as file:
                for i in range(self.task_listbox.size()):
                    file.write(self.task_listbox.get(i) + "\n")
            messagebox.showinfo("Save", "Tasks saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save tasks.\n{e}")

    def load_tasks(self):
        try:
            with open(self.task_file, "r") as file:
                self.task_listbox.delete(0, tk.END)
                for line in file:
                    self.task_listbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            open(self.task_file, "w").close()  # Create file if not exists
        except Exception as e:
            messagebox.showerror("Error", f"Could not load tasks.\n{e}")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        bg_color = "#2e2e2e" if self.is_dark else "#ffffff"
        fg_color = "#ffffff" if self.is_dark else "#000000"

        self.root.configure(bg=bg_color)
        widgets = [
            self.header, self.task_entry, self.add_button,
            self.task_listbox, self.done_button,
            self.delete_button, self.save_button,
            self.load_button, self.theme_button
        ]

        for widget in widgets:
            widget.configure(bg=bg_color, fg=fg_color)

        self.task_listbox.configure(selectbackground="#444" if self.is_dark else "#ccc")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
