import os  # for checking files
import csv  # for reading/writing CSV files
import tkinter as tk  # for GUI
from tkinter import ttk, messagebox, simpledialog  # GUI helper modules

DATA_FILENAME = "students.txt"  # the file where student data is stored


# Helper: grade calculation
def calc_percentage_and_grade(c1, c2, c3, exam):
    # calculate total marks and percentage
    total_coursework = c1 + c2 + c3
    total_marks = total_coursework + exam
    max_marks = 20 * 3 + 100
    percentage = round(total_marks / max_marks * 100)
    
    # assign letter grade
    if percentage >= 90:
        grade = "A"
    elif percentage >= 80:
        grade = "B"
    elif percentage >= 70:
        grade = "C"
    elif percentage >= 60:
        grade = "D"
    else:
        grade = "F"
    return percentage, grade

# Load / Save functions
def load_students(filename=DATA_FILENAME):
    students = []
    if not os.path.isfile(filename):
        return students  # return empty if file doesn't exist
    # open the file and read all students
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for parts in reader:
            if not parts or len(parts) < 6:
                continue
            try:
                number = int(parts[0].strip())
                name = parts[1].strip()
                c1 = int(parts[2].strip())
                c2 = int(parts[3].strip())
                c3 = int(parts[4].strip())
                exam = int(parts[5].strip())
            except ValueError:
                continue
            percentage, grade = calc_percentage_and_grade(c1, c2, c3, exam)
            # add student as dictionary
            students.append({
                "number": number,
                "name": name,
                "course1": c1,
                "course2": c2,
                "course3": c3,
                "exam": exam,
                "percentage": percentage,
                "grade": grade
            })
    return students

def save_students(students, filename=DATA_FILENAME):
    # save all student records to file
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for s in students:
            writer.writerow([s["number"], s["name"], s["course1"], s["course2"], s["course3"], s["exam"]])

# UI functions
def display_student(student):
    output_box.delete(1.0, tk.END)  # clear text box
    # show student info
    output_box.insert(tk.END, f"Name: {student['name']}\n")
    output_box.insert(tk.END, f"Number: {student['number']}\n")
    output_box.insert(tk.END, f"Course 1: {student['course1']}\n")
    output_box.insert(tk.END, f"Course 2: {student['course2']}\n")
    output_box.insert(tk.END, f"Course 3: {student['course3']}\n")
    output_box.insert(tk.END, f"Exam: {student['exam']}\n")
    output_box.insert(tk.END, f"Overall Percentage: {student['percentage']}%\n")
    output_box.insert(tk.END, f"Grade: {student['grade']}\n")

def view_all_records():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No student records.\n")
        return
    # show all students
    for s in students:
        output_box.insert(tk.END, f"Name: {s['name']}\n")
        output_box.insert(tk.END, f"Number: {s['number']}\n")
        output_box.insert(tk.END, f"Course 1: {s['course1']}\n")
        output_box.insert(tk.END, f"Course 2: {s['course2']}\n")
        output_box.insert(tk.END, f"Course 3: {s['course3']}\n")
        output_box.insert(tk.END, f"Exam: {s['exam']}\n")
        output_box.insert(tk.END, f"Overall Percentage: {s['percentage']}%\n")
        output_box.insert(tk.END, f"Grade: {s['grade']}\n")
        output_box.insert(tk.END, "-"*45 + "\n")

def show_highest_score():
    if not students:
        messagebox.showinfo("Info", "No students loaded.")
        return
    # show student with highest percentage
    display_student(max(students, key=lambda s: s["percentage"]))

def show_lowest_score():
    if not students:
        messagebox.showinfo("Info", "No students loaded.")
        return
    # show student with lowest percentage
    display_student(min(students, key=lambda s: s["percentage"]))

def search_by_number():
    txt = student_number_entry.get().strip()
    if not txt:
        messagebox.showwarning("Input required", "Enter a student number to search.")
        return
    try:
        num = int(txt)
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a valid numeric student number.")
        return
    # find student by number
    for s in students:
        if s["number"] == num:
            display_student(s)
            return
    messagebox.showinfo("Not found", f"No student with number {num}.")

def add_student_dialog():
    try:
        # ask user to input new student info
        number = simpledialog.askinteger("New Student", "Enter student number:")
        if number is None: return
        name = simpledialog.askstring("New Student", "Enter student's full name:")
        if name is None: return
        c1 = simpledialog.askinteger("New Student", "Course 1 mark (0-20):")
        if c1 is None: return
        c2 = simpledialog.askinteger("New Student", "Course 2 mark (0-20):")
        if c2 is None: return
        c3 = simpledialog.askinteger("New Student", "Course 3 mark (0-20):")
        if c3 is None: return
        exam = simpledialog.askinteger("New Student", "Exam mark (0-100):")
        if exam is None: return
    except Exception:
        messagebox.showwarning("Invalid", "One or more fields are invalid.")
        return
    percentage, grade = calc_percentage_and_grade(c1, c2, c3, exam)
    new_student = {
        "number": number,
        "name": name.strip(),
        "course1": c1,
        "course2": c2,
        "course3": c3,
        "exam": exam,
        "percentage": percentage,
        "grade": grade
    }
    students.append(new_student)
    save_students(students)
    messagebox.showinfo("Saved", f"Student {name} added and saved to {DATA_FILENAME}.")

def exit_program():
    # close the program
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        root.destroy()

# Build GUI

root = tk.Tk()
root.title("Student Manager")
root.geometry("700x520")
root.configure(bg="black")

TITLE_FONT = ("Segoe UI Semibold", 20, "bold")
LABEL_FONT = ("Segoe UI Semibold", 10)
BTN_FONT = ("Segoe UI Semibold", 10)
TEXT_FONT = ("Consolas", 10)

# Title label
title_label = tk.Label(root, text="STUDENT MANAGER", font=TITLE_FONT, bg="black", fg="white")
title_label.pack(pady=12)

# Top buttons frame
top_frame = tk.Frame(root, bg="black")
top_frame.pack(pady=6)

def make_button(parent, text, command):
    # helper function to create buttons
    return tk.Button(parent, text=text, command=command, font=BTN_FONT, width=22, height=2,
                     bg="white", fg="black", activebackground="#cccccc")

# Buttons
view_all_btn = make_button(top_frame, "View All Student Records", view_all_records)
highest_btn = make_button(top_frame, "Show Highest Score", show_highest_score)
lowest_btn = make_button(top_frame, "Show Lowest Score", show_lowest_score)
view_all_btn.grid(row=0, column=0, padx=6, pady=5)
highest_btn.grid(row=0, column=1, padx=6, pady=5)
lowest_btn.grid(row=0, column=2, padx=6, pady=5)

# Middle search and add frame
middle_frame = tk.Frame(root, bg="black")
middle_frame.pack(pady=18)

search_label = tk.Label(middle_frame, text="Search by Student Number:", font=LABEL_FONT, bg="black", fg="white")
search_label.grid(row=0, column=0, padx=6)
student_number_entry = tk.Entry(middle_frame, font=LABEL_FONT, width=25)
student_number_entry.grid(row=0, column=1, padx=6)
search_btn = make_button(middle_frame, "Search", search_by_number)
search_btn.grid(row=0, column=2, padx=6)
add_btn = make_button(middle_frame, "Add New Student", add_student_dialog)
add_btn.grid(row=1, column=1, pady=10)

# Output box
output_box = tk.Text(root, height=14, width=85, font=TEXT_FONT, bg="black", fg="white")
output_box.pack(pady=6)

# Bottom exit button
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(pady=6)
exit_btn = make_button(bottom_frame, "Exit Program", exit_program)
exit_btn.grid(row=0, column=0, padx=6)

# Footer label
footer_label = tk.Label(root, text="Created by Clint | Student Manager v2.0",
                        font=("Segoe UI", 9, "italic"), bg="black", fg="white")
footer_label.pack(side="bottom", pady=6)

# Load students and start GUI
students = load_students()  # read student data from file
root.mainloop()  # start the program
