import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

def save_data():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    gender = gender_var.get()
    department = entry_department.get().strip()
    college_name = entry_college.get().strip()

    if not (name and age and gender and department and college_name):
        messagebox.showerror("Error", "Please fill all fields")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Please enter a valid positive integer for age.")
        return

    file_exists = os.path.isfile('students.csv')
    with open('students.csv', 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Age', 'Gender', 'Department', 'College Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'Name': name,
            'Age': age,
            'Gender': gender,
            'Department': department,
            'College Name': college_name
        })

    messagebox.showinfo("Success", "Student data saved successfully!")

    # Clear fields
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    gender_var.set('')
    entry_department.delete(0, tk.END)
    entry_college.delete(0, tk.END)
    entry_name.focus()


# --- Main Window Setup ---
root = tk.Tk()
root.title("Student Bio Data")
root.geometry("500x400")  # Small height to demonstrate scrolling
root.configure(bg="#1B263B")

# Scrollable Canvas and Frame Setup
container = ttk.Frame(root)
canvas = tk.Canvas(container, bg="#1B263B", highlightthickness=0)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Styling
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#1B263B", foreground="#E0E0E0", font=("Segoe UI", 12))
style.configure("TEntry", font=("Segoe UI", 12), padding=6)
style.configure("TRadiobutton", background="#1B263B", foreground="#E0E0E0", font=("Segoe UI", 12))
style.configure("TButton",
                font=("Segoe UI", 13, "bold"),
                padding=10,
                foreground="#FFFFFF",
                background="#2874A6")
style.map("TButton",
          foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF')],
          background=[('pressed', '#1F618D'), ('active', '#5499C7')])

# Labels and Inputs with Grid
def create_labeled_entry(row, label_text):
    ttk.Label(scrollable_frame, text=label_text).grid(row=row, column=0, padx=20, pady=10, sticky="w")
    entry = ttk.Entry(scrollable_frame, width=35)
    entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
    return entry

entry_name = create_labeled_entry(0, "Name")
entry_age = create_labeled_entry(1, "Age")

# Gender
ttk.Label(scrollable_frame, text="Gender").grid(row=2, column=0, padx=20, pady=10, sticky="w")
gender_var = tk.StringVar(value='')
gender_frame = ttk.Frame(scrollable_frame)
gender_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side='left', padx=5)
ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side='left', padx=5)
ttk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other").pack(side='left', padx=5)

entry_department = create_labeled_entry(3, "Department")
entry_college = create_labeled_entry(4, "College Name")  # For NIT or any other college

# Submit Button
submit_btn = ttk.Button(scrollable_frame, text="Submit", command=save_data)
submit_btn.grid(row=5, column=0, columnspan=2, pady=30, ipadx=80)

entry_name.focus()

root.mainloop()
