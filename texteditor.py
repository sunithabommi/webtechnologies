import tkinter as tk
from tkinter import messagebox
import csv

class StudentRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management")
        self.root.geometry("500x400")

        # Define file path for CSV
        self.csv_file = "students.csv"

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.age_label = tk.Label(self.root, text="Age:")
        self.age_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.grade_label = tk.Label(self.root, text="Grade:")
        self.grade_label.grid(row=2, column=0, padx=10, pady=10)

        # Entry widgets
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.grade_entry = tk.Entry(self.root)
        self.grade_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        self.add_button = tk.Button(self.root, text="Add Student", command=self.add_student)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.show_button = tk.Button(self.root, text="Show Students", command=self.show_students)
        self.show_button.grid(row=3, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Student", command=self.delete_student)
        self.delete_button.grid(row=3, column=2, padx=10, pady=10)

        # Listbox to display students
        self.student_listbox = tk.Listbox(self.root, width=50, height=10)
        self.student_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()

        if not name or not age or not grade:
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        # Append the new student data to the CSV file
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, age, grade])
        
        # Clear the input fields
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Student added successfully!")

    def show_students(self):
        # Clear current listbox
        self.student_listbox.delete(0, tk.END)

        try:
            with open(self.csv_file, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.student_listbox.insert(tk.END, f"Name: {row[0]}, Age: {row[1]}, Grade: {row[2]}")
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "No student data file found. Please add a student first.")

    def delete_student(self):
        selected_student = self.student_listbox.curselection()

        if not selected_student:
            messagebox.showerror("Selection Error", "Please select a student to delete.")
            return
        
        # Get the selected student data
        selected_student_data = self.student_listbox.get(selected_student)
        student_name = selected_student_data.split(",")[0].split(":")[1].strip()

        # Read all students from the CSV file
        students = []
        with open(self.csv_file, mode="r") as file:
            reader = csv.reader(file)
            students = list(reader)

        # Remove the student with the selected name
        students = [student for student in students if student[0] != student_name]

        # Write the updated students list back to the CSV
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(students)

        # Refresh the student list
        self.show_students()
        messagebox.showinfo("Success", f"Student {student_name} deleted successfully!")

# Create the main window
root = tk.Tk()
app = StudentRecordApp(root)

# Start the Tkinter event loop
root.mainloop()
