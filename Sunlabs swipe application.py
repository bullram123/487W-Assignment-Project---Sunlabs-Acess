import tkinter as tk
import mysql.connector
from datetime import datetime

# Function to create a database connection
def get_database_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sun_lab'
    )

# Create the database and tables
def create_database_and_tables():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Create the database if it doesn't exist with character set and collation
        cursor.execute("CREATE DATABASE IF NOT EXISTS sun_lab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

        # Switch to the 'sun_lab' database
        cursor.execute("USE sun_lab")

        # Create the 'students' table if it doesn't exist with the 'user_type' column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(9) UNIQUE,
                user_type ENUM('student', 'faculty') NOT NULL
            )
        """)

        # Create the 'login_timestamps' table to store login timestamps
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_timestamps (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                login_time TIMESTAMP
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

def insert_sample_data():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert sample student and faculty data with user_type and status
        data = [
            ('123456789', 'student', 'active'),
            ('987654321', 'student', 'active'),
            ('555555555', 'faculty', 'active'),
            ('666666666', 'faculty', 'active'),
            ('777777777', 'student', 'active'),  # Additional student
            ('888888888', 'faculty', 'active'),  # Additional faculty
        ]
        cursor.executemany("INSERT INTO students (student_id, user_type, status) VALUES (%s, %s, %s)", data)

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Function to insert a login timestamp into the 'login_timestamps' table
def insert_login_timestamp(user_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert the login timestamp with the current time
        login_time = datetime.now()
        cursor.execute("INSERT INTO login_timestamps (user_id, login_time) VALUES (%s, %s)", (user_id, login_time))

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Function to open a student window
def open_student_window():
    # Create a new window for students
    student_window = tk.Toplevel(root)
    student_window.title("Student Window")

    # Add content to the student window
    label = tk.Label(student_window, text="Welcome CMSPC member you swiped in/out!", font=("Helvetica", 14))
    label.pack()

# Function to search for a specific user's login timestamp
def search_timestamp(user_id, faculty_window):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT login_time FROM login_timestamps WHERE user_id IN (SELECT id FROM students WHERE student_id = %s)", (user_id,))
        timestamps = cursor.fetchall()

        if timestamps:
            timestamp_label = tk.Label(faculty_window, text=f"Timestamps for {user_id}:", font=("Helvetica", 12))
            timestamp_label.pack()
            for timestamp in timestamps:
                timestamp_info = f"Timestamp: {timestamp[0]}"
                timestamp_label = tk.Label(faculty_window, text=timestamp_info, font=("Helvetica", 12))
                timestamp_label.pack()
        else:
            timestamp_label = tk.Label(faculty_window, text=f"No timestamps found for {user_id}", font=("Helvetica", 12))
            timestamp_label.pack()

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Create a global variable for faculty_window
faculty_window = None

def open_faculty_window():
    global faculty_window  # Declare faculty_window as a global variable
    if faculty_window is None or not faculty_window.winfo_exists():
        faculty_window = tk.Toplevel(root)
        faculty_window.title("Faculty Window")

        # Create a frame to organize content
        frame = tk.Frame(faculty_window)
        frame.pack(expand=True, fill="both")

        # Add content to the faculty window
        label = tk.Label(frame, text="Welcome, Faculty!", font=("Helvetica", 14))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create entry and button for searching user timestamps
        search_label = tk.Label(frame, text="Enter 9-digit ID to search timestamp:", font=("Helvetica", 12))
        search_entry = tk.Entry(frame, font=("Helvetica", 12))
        search_button = tk.Button(frame, text="Search", command=lambda: search_timestamp(search_entry.get(), faculty_window), font=("Helvetica", 12))
        search_label.grid(row=1, column=0, padx=10, pady=5)
        search_entry.grid(row=1, column=1, padx=10, pady=5)
        search_button.grid(row=1, column=2, padx=10, pady=5)

        # Create entry and button for creating a new student
        create_label = tk.Label(frame, text="Enter 9-digit ID to activate the student:", font=("Helvetica", 12))
        create_entry = tk.Entry(frame, font=("Helvetica", 12))
        create_button = tk.Button(frame, text="Activate new student Student", command=lambda: create_student(create_entry.get()), font=("Helvetica", 12))
        create_label.grid(row=2, column=0, padx=10, pady=5)
        create_entry.grid(row=2, column=1, padx=10, pady=5)
        create_button.grid(row=2, column=2, padx=10, pady=5)

        # Create entry and button for deleting a student
        delete_label = tk.Label(frame, text="Enter 9-digit ID to delete a student:", font=("Helvetica", 12))
        delete_entry = tk.Entry(frame, font=("Helvetica", 12))
        delete_button = tk.Button(frame, text="Suspend Student", command=lambda: delete_student(delete_entry.get()), font=("Helvetica", 12))
        delete_label.grid(row=3, column=0, padx=10, pady=5)
        delete_entry.grid(row=3, column=1, padx=10, pady=5)
        delete_button.grid(row=3, column=2, padx=10, pady=5)

        # Create entry and button for deactivating a student
        deactivate_label = tk.Label(frame, text="Enter 9-digit ID to deactivate a student:", font=("Helvetica", 12))
        deactivate_entry = tk.Entry(frame, font=("Helvetica", 12))
        deactivate_button = tk.Button(frame, text="Deactivate Student", command=lambda: deactivate_student(deactivate_entry.get()), font=("Helvetica", 12))
        deactivate_label.grid(row=5, column=0, padx=10, pady=5)  # Adjusted row value
        deactivate_entry.grid(row=5, column=1, padx=10, pady=5)  # Adjusted row value
        deactivate_button.grid(row=5, column=2, padx=10, pady=5)  # Adjusted row value


        # Create a scrollbar for the user list
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        user_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
        user_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        scrollbar.config(command=user_listbox.yview)
        scrollbar.grid(row=4, column=3, sticky="ns")

        # Set row and column weights for frame to expand properly
        for i in range(5):
            frame.rowconfigure(i, weight=1)
        for i in range(4):
            frame.columnconfigure(i, weight=1)

        # Refresh the user list when the faculty window is opened
        faculty_window.bind("<Map>", lambda event: populate_user_list(user_listbox))

        # Populate the user list initially
        populate_user_list(user_listbox)


def populate_user_list(user_listbox):
    user_listbox.delete(0, tk.END)
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT students.student_id, students.user_type, login_timestamps.login_time
            FROM students
            LEFT JOIN login_timestamps ON students.id = login_timestamps.user_id
        """)

        users = cursor.fetchall()

        if users:
            for user in users:
                user_info = f"ID: {user[0]}, Type: {user[1]}, Timestamp: {user[2]}"
                user_listbox.insert(tk.END, user_info)

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Function to create a new student and add them to the database
def create_student(student_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Check if the student ID already exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        existing_student = cursor.fetchone()

        if existing_student:
            status.config(text="Student ID already exists")
        else:
            # Insert the new student into the 'students' table
            cursor.execute("INSERT INTO students (student_id, user_type) VALUES (%s, 'student')", (student_id,))
            connection.commit()
            status.config(text="Student created successfully")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Function to delete a student from the database
def delete_student(student_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Check if the student ID exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        existing_student = cursor.fetchone()

        if existing_student:
            # Delete the student from the 'students' table
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            connection.commit()
            status.config(text="Student deleted successfully")
        else:
            status.config(text="Student ID not found")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)

# Function to handle student login
def student_login():
    student_id = entry.get()
    if len(student_id) == 9 and student_id.isdigit():
        # Check if the student ID exists in the database
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            user_data = cursor.fetchone()

            if user_data:
                insert_login_timestamp(user_data[0])  # Insert login timestamp
                open_student_window()  # Student login opens a student window
            else:
                status.config(text="Invalid student ID")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print("Error:", err)
    else:
        status.config(text="Invalid student ID")

# Function to handle faculty login
def faculty_login():
    faculty_id = entry.get()
    if len(faculty_id) == 9 and faculty_id.isdigit():
        # Check if the faculty ID exists in the database
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s AND user_type = 'faculty'", (faculty_id,))
            user_data = cursor.fetchone()

            if user_data:
                open_faculty_window()  # Faculty login opens the faculty window
            else:
                status.config(text="Invalid faculty ID")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print("Error:", err)
    else:
        status.config(text="Invalid faculty ID")

# Create the main Tkinter window
root = tk.Tk()
root.title("SUN Lab Login")

# Improve the UI appearance
root.geometry("500x300")  # Set the initial window size

# Create and configure widgets with better styling
label = tk.Label(root, text="Enter your 9-digit ID:", font=("Helvetica", 14))
entry = tk.Entry(root, font=("Helvetica", 12))
student_login_button = tk.Button(root, text="General Log-in (you will swipe in and out to log your time in and out)", command=student_login, font=("Helvetica", 12))
faculty_login_button = tk.Button(root, text="Faculty Login for faculty who needs to see records", command=faculty_login, font=("Helvetica", 12))
status = tk.Label(root, text="", font=("Helvetica", 12), fg="red")

# Grid layout
label.grid(row=0, column=0, padx=10, pady=5, columnspan=2)
entry.grid(row=1, column=0, padx=10, pady=5, columnspan=2)
student_login_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky='ew')
faculty_login_button.grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky='ew')
status.grid(row=4, column=0, columnspan=2, pady=5)

# Set column weights to expand horizontally
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Create the database and tables
create_database_and_tables()

# Insert sample student and faculty data into the database
insert_sample_data()

# Start the main loop
root.mainloop()