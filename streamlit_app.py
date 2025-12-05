import streamlit as st
from sqlalchemy import text

def main():
    st.title('Student Management System')

    conn = st.connection("postgresql", type="sql")

    # Display existing students
    st.header('Current Students')
    df = conn.query('SELECT * FROM students;', ttl=0)
    st.write(df)

    # Form to add new student
    st.header('Add New Student')
    with st.form("add_student_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        student_number = st.text_input("Student Number")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if first_name and last_name and email and student_number:
                with conn.session as s:
                    s.execute(
                        text("""
                            INSERT INTO students (first_name, last_name, email, student_number)
                            VALUES (:p1, :p2, :p3, :p4)
                        """),
                        {"p1": first_name, "p2": last_name, "p3": email, "p4": student_number}
                    )
                    s.commit()
                st.success(f"Successfully added student: {first_name} {last_name}")
                st.rerun()
            else:
                st.error("Please fill in all fields")

if __name__ == "__main__":
    main()
