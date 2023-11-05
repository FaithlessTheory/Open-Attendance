import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime

attendance_file = "attendance.txt"
class_schedule_file = "class_schedule.txt"
class_schedule = {}

def load_class_schedule():
    if os.path.exists(class_schedule_file):
        with open(class_schedule_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    class_name, class_details = parts
                    class_details = class_details.split(", ")
                    if len(class_details) >= 3:
                        start_time, end_time, days = class_details[:3]
                        class_schedule[class_name] = (start_time, end_time, days)

def save_class_schedule():
    with open(class_schedule_file, "w") as file:
        for class_name, (start_time, end_time, days) in class_schedule.items():
            file.write(f"{class_name}: {start_time}, {end_time}, {days}\n")

def take_attendance():
    student_name = student_name_entry.get()
    selected_class = class_var.get()
    current_time = datetime.now().strftime("%H:%M")
    with open(attendance_file, "a") as file:
        file.write(f"{student_name} ({selected_class}, {current_time})\n")
    student_name_entry.delete(0, tk.END)

def view_attendance():
    if os.path.exists(attendance_file):
        with open(attendance_file, "r") as file:
            attendance_list = file.read()
            attendance_text.config(state=tk.NORMAL)
            attendance_text.delete(1.0, tk.END)
            attendance_text.insert(tk.END, attendance_list)
            attendance_text.config(state=tk.DISABLED)
    else:
        attendance_text.config(state=tk.NORMAL)
        attendance_text.delete(1.0, tk.END)
        attendance_text.insert(tk.END, "No attendance data found.")
        attendance_text.config(state=tk.DISABLED)

def open_class_schedule():
    if os.path.exists(class_schedule_file):
        with open(class_schedule_file, "r") as file:
            class_schedule_text.config(state=tk.NORMAL)
            class_schedule_text.delete(1.0, tk.END)
            class_schedule_text.insert(tk.END, file.read())
            class_schedule_text.config(state=tk.DISABLED)
    else:
        class_schedule_text.config(state=tk.NORMAL)
        class_schedule_text.delete(1.0, tk.END)
        class_schedule_text.insert(tk.END, "No class schedule data found.")
        class_schedule_text.config(state=tk.DISABLED)

def update_class_schedule():
    class_name = update_class_name_var.get()
    start_time = update_start_time_var.get()
    end_time = update_end_time_var.get()
    days = update_days_var.get()
    
    if class_name:
        class_schedule[class_name] = (start_time, end_time, days)
        save_class_schedule()
    update_class_name_entry.delete(0, tk.END)
    update_start_time_entry.delete(0, tk.END)
    update_end_time_entry.delete(0, tk.END)
    update_days_entry.delete(0, tk.END)

def check_missing_classes():
    present_classes = set()
    if os.path.exists(attendance_file):
        with open(attendance_file, "r") as file:
            attendance_list = file.readlines()
            for entry in attendance_list:
                parts = entry.split('(')
                if len(parts) > 1:
                    class_time = parts[1].split(',')[1].strip().replace(")", "")
                    present_classes.add((parts[0], class_time))

    missing_classes = []
    for class_name, (start_time, end_time, days) in class_schedule.items():
        current_day = datetime.now().strftime("%A")
        if current_day in days.split(", "):
            if (class_name, start_time) not in present_classes:
                missing_classes.append((class_name, start_time))

    return missing_classes

# Load the class schedule from the file
load_class_schedule()

# Create the main window
root = tk.Tk()
root.title("School Attendance System")

# Create a notebook with two tabs
notebook = ttk.Notebook(root)

# Create the first tab for attendance
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Attendance")

# Create and configure widgets for the first tab
student_name_label = tk.Label(tab1, text="Enter the student's name:")
student_name_entry = tk.Entry(tab1)
class_label = tk.Label(tab1, text="Select Class:")
class_var = tk.StringVar(value=list(class_schedule.keys())[0])
class_dropdown = tk.OptionMenu(tab1, class_var, *class_schedule.keys())
take_attendance_button = tk.Button(tab1, text="Take Attendance", command=take_attendance)
view_attendance_button = tk.Button(tab1, text="View Attendance", command=view_attendance)
attendance_text = tk.Text(tab1, state=tk.DISABLED, width=40, height=10)

# Pack widgets for the first tab
student_name_label.pack()
student_name_entry.pack()
class_label.pack()
class_dropdown.pack()
take_attendance_button.pack()
view_attendance_button.pack()
attendance_text.pack()

# Create the second tab for class schedule
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Class Schedule")

# Create and configure widgets for the second tab
open_schedule_button = tk.Button(tab2, text="Open Class Schedule", command=open_class_schedule)
class_schedule_text = tk.Text(tab2, state=tk.DISABLED, width=40, height=10)

# Create and configure widgets for updating class schedule
update_class_name_label = tk.Label(tab2, text="Class Name:")
update_class_name_var = tk.StringVar()
update_class_name_entry = tk.Entry(tab2, textvariable=update_class_name_var)
update_start_time_label = tk.Label(tab2, text="Start Time:")
update_start_time_var = tk.StringVar()
update_start_time_entry = tk.Entry(tab2, textvariable=update_start_time_var)
update_end_time_label = tk.Label(tab2, text="End Time:")
update_end_time_var = tk.StringVar()
update_end_time_entry = tk.Entry(tab2, textvariable=update_end_time_var)
update_days_label = tk.Label(tab2, text="Days (comma-separated):")
update_days_var = tk.StringVar()
update_days_entry = tk.Entry(tab2, textvariable=update_days_var)
update_schedule_button = tk.Button(tab2, text="Update Class Schedule", command=update_class_schedule)

# Pack widgets for the second tab
open_schedule_button.pack()
class_schedule_text.pack()
update_class_name_label.pack()
update_class_name_entry.pack()
update_start_time_label.pack()
update_start_time_entry.pack()
update_end_time_label.pack()
update_end_time_entry.pack()
update_days_label.pack()
update_days_entry.pack()
update_schedule_button.pack()

# Start the main loop
notebook.pack(expand=1, fill="both")
root.mainloop()
