# TalkDB: Natural Language to PostgreSQL 🗄️

TalkDB is an AI-powered database interface that allows users to query a university database using plain English. Built with Streamlit and powered by Google's Gemini 2.5 Flash, it seamlessly translates conversational questions into precise, case-sensitive PostgreSQL queries. The app executes these queries against a live Supabase cloud database and returns the results in a clean, interactive data table.

## ✨ Features
* **Natural Language Processing:** Ask questions like *"Show me all students in Computer Science"* and get instant data.
* **Cloud Database Integration:** Fully integrated with a live PostgreSQL database hosted on Supabase, bypassing local SQLite limitations.
* **Smart SQL Generation:** Uses prompt engineering to force strict PostgreSQL dialects and case-sensitive table queries.
* **Secure Execution:** Built-in application safeguards to ensure only read-only `SELECT` queries are executed, protecting the database from destructive commands.
* **Interactive UI:** A clean, responsive frontend built with Streamlit and Pandas dataframes.

## 🛠️ Tech Stack
* **Frontend UI:** Streamlit
* **Backend Logic:** Python
* **AI Model:** Google Gemini 2.5 Flash
* **Cloud Database:** PostgreSQL (Supabase)
* **Libraries:** `psycopg2-binary`, `pandas`, `google-generativeai`, `python-dotenv`

## 🚀 Local Setup & Installation

Follow these steps to run TalkDB on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Vivoboy11/TalkDB.git](https://github.com/Vivoboy11/TalkDB.git)
cd TalkDB
# Create the environment
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
GEMINI_API_KEY="your_google_gemini_api_key"
DATABASE_URL="postgresql://username:password@your-supabase-pooler-url:6543/postgres?sslmode=require"
-- Create Tables
CREATE TABLE "Students" (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    major TEXT,
    enrollment_year INTEGER
);

CREATE TABLE "Courses" (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    department TEXT,
    credits INTEGER
);

CREATE TABLE "Enrollments" (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES "Students"(student_id),
    course_id INTEGER REFERENCES "Courses"(course_id),
    grade TEXT
);

-- Insert Mock Data
INSERT INTO "Students" (student_id, name, major, enrollment_year) VALUES
(1, 'Neha Gupta', 'Artificial Intelligence', 2025),
(2, 'Rahul Sharma', 'Computer Science', 2024),
(3, 'Priya Patel', 'Data Science', 2023);

INSERT INTO "Courses" (course_id, course_name, department, credits) VALUES
(1, 'Machine Learning', 'AI', 4),
(2, 'Database Systems', 'CS', 3),
(3, 'Data Mining', 'DS', 3);

INSERT INTO "Enrollments" (enrollment_id, student_id, course_id, grade) VALUES
(1, 1, 1, 'A'),
(2, 2, 2, 'B'),
(3, 3, 3, 'A');
for checking if application is working or not
streamlit run app.py
 created by:
 Raj Gulab Singh

GitHub: @Vivoboy11