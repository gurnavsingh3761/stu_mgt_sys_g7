import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

st.title("Student Record Management System")

# CREATE
st.subheader("Add Student")

roll = st.number_input("Roll Number", min_value=1, step=1)
name = st.text_input("Student Name")
age = st.number_input("Age", min_value=1, max_value=100, step=1)
course = st.text_input("Course")

if st.button("Add Student"):
    if name and course:
        try:
            cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?)",
                (roll, name, age, course)
            )
            conn.commit()
            st.success("Student Added Successfully!")
        except sqlite3.IntegrityError:
            st.error("Roll Number already exists!")
    else:
        st.warning("Please fill all fields.")

# READ
st.subheader("View Students")

df = pd.read_sql_query("SELECT * FROM students", conn)
st.dataframe(df, use_container_width=True)

# UPDATE
st.subheader("Update Student")

update_roll = st.number_input(
    "Enter Roll Number to Update", min_value=1, step=1, key="update"
)

new_name = st.text_input("New Name")
new_age = st.number_input("New Age", min_value=1, max_value=100, step=1)
new_course = st.text_input("New Course")

if st.button("Update Student"):
    cursor.execute("""
        UPDATE students
        SET name=?, age=?, course=?
        WHERE roll_no=?
    """, (new_name, new_age, new_course, update_roll))

    conn.commit()

    if cursor.rowcount > 0:
        st.success("Student Updated Successfully!")
    else:
        st.error("Student Not Found!")

# DELETE
st.subheader("Delete Student")

delete_roll = st.number_input(
    "Enter Roll Number to Delete", min_value=1, step=1, key="delete"
)

if st.button("Delete Student"):
    cursor.execute(
        "DELETE FROM students WHERE roll_no=?",
        (delete_roll,)
    )
    conn.commit()

    if cursor.rowcount > 0:
        st.success("Student Deleted Successfully!")
    else:
        st.error("Student Not Found!")

# Close connection when script finishes
conn.close()