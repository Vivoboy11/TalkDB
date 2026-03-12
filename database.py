import sqlite3
import pandas as pd

DB_NAME = "talkdb.sqlite"

def setup_database():
    """Creates the tables and populates them with initial dummy data."""
    # 1. Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 2. Define the Schema (DDL - Data Definition Language)
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            major TEXT NOT NULL,
            enrollment_year INTEGER
        );

        CREATE TABLE IF NOT EXISTS Courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            department TEXT NOT NULL,
            credits INTEGER
        );

        CREATE TABLE IF NOT EXISTS Enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            grade TEXT,
            FOREIGN KEY(student_id) REFERENCES Students(student_id),
            FOREIGN KEY(course_id) REFERENCES Courses(course_id)
        );
    ''')

    # 3. Insert Dummy Data (DML - Data Manipulation Language)
    # We first check if data already exists so we don't duplicate it on multiple runs
    cursor.execute("SELECT COUNT(*) FROM Students")
    if cursor.fetchone()[0] == 0:
        cursor.executescript('''
            INSERT INTO Students (name, major, enrollment_year) VALUES 
                ('Aarav Patel', 'Computer Science', 2024),
                ('Priya Sharma', 'Data Science', 2025),
                ('Rohan Desai', 'Computer Science', 2024),
                ('Neha Gupta', 'Artificial Intelligence', 2025);

            INSERT INTO Courses (course_name, department, credits) VALUES 
                ('Theory of Computation', 'Computer Science', 4),
                ('Database Management Systems', 'Computer Science', 3),
                ('Operating Systems', 'Computer Science', 4);

            INSERT INTO Enrollments (student_id, course_id, grade) VALUES 
                (1, 2, 'A'), (1, 3, 'B+'),
                (2, 2, 'A+'),
                (3, 1, 'B'), (3, 3, 'A-'),
                (4, 2, 'A');
        ''')
        print("Mock data successfully inserted!")
    else:
        print("Database already populated. Ready to go!")

    conn.commit()
    conn.close()

def run_query(sql_query):
    """
    Executes a raw SQL query and returns a Pandas DataFrame.
    This is the function our AI will eventually call!
    """
    conn = sqlite3.connect(DB_NAME)
    try:
        # We use pandas here because Streamlit renders DataFrames beautifully
        df = pd.read_sql_query(sql_query, conn)
        return df
    except Exception as e:
        return f"Error executing query: {e}"
    finally:
        conn.close()

# Run the setup function when this file is executed directly
if __name__ == "__main__":
    setup_database()