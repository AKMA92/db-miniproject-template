import streamlit as st

def main():
    st.title("Miniproject App")
    
    # Initialize connection.
    conn = st.connection("postgresql", type="sql")

    # Perform query.
    df = conn.query('SELECT * FROM students;')

    st.write(df)

if __name__ == "__main__":
    main()
