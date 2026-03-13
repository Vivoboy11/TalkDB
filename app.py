import streamlit as st
import pandas as pd
import google.generativeai as genai
import psycopg2
import os
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. The System Prompt: Teaching the AI your DBMS Schema
# Changed "SQLite" to "PostgreSQL" so it writes the exact right SQL dialect.
SCHEMA_PROMPT = """
You are an expert PostgreSQL translator. Your job is to translate plain English into SQL queries for a PostgreSQL database.
Here is the schema of the database:

Table: Students
Columns: student_id (INTEGER PRIMARY KEY), name (TEXT), major (TEXT), enrollment_year (INTEGER)

Table: Courses
Columns: course_id (INTEGER PRIMARY KEY), course_name (TEXT), department (TEXT), credits (INTEGER)

Table: Enrollments
Columns: enrollment_id (INTEGER PRIMARY KEY), student_id (INTEGER, FOREIGN KEY), course_id (INTEGER, FOREIGN KEY), grade (TEXT)

Rules:
1. Output ONLY the raw SQL query. No markdown formatting, no explanations.
2. Only write SELECT queries. Never write DROP, UPDATE, DELETE, or INSERT.
"""

def get_sql_from_ai(user_question):
    """Sends the user's question and our schema to Gemini to get a SQL query."""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    prompt = SCHEMA_PROMPT + f"\n\nUser Question: {user_question}\nSQL Query:"
    response = model.generate_content(prompt)

    return response.text.strip()

# 3. Streamlit Frontend UI
st.set_page_config(page_title="TalkDB", page_icon="🗄️")
st.title("TalkDB: Natural Language to SQL")
st.write("Ask a question in plain English, and the AI will query the University database.")

# Text input for the user
user_input = st.text_input("What would you like to know? (e.g., 'Show me all students in Computer Science')")

if st.button("Query Database"):
    if user_input:
        with st.spinner("Translating to SQL..."):
            try:
                # Get the SQL string from Gemini
                sql_query = get_sql_from_ai(user_input)
                
                # Clean up any markdown the AI might accidentally include
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                
                st.write("**Generated SQL Query:**")
                st.code(sql_query, language="sql")

                # Security check: Prevent destructive database commands
                if not sql_query.upper().startswith("SELECT"):
                    st.error("Security Alert: Only SELECT queries are allowed!")
                else:
                    # NEW POSTGRESQL CONNECTION LOGIC
                    db_url = os.environ.get("DATABASE_URL")
                    conn = psycopg2.connect(db_url)
                    
                    try:
                        # pandas can read SQL directly if we give it the connection!
                        results_df = pd.read_sql_query(sql_query, conn)
                        
                        # Display the results
                        if results_df.empty:
                            st.warning("Query ran successfully, but no results were found.")
                        else:
                            st.success("Results fetched successfully!")
                            st.dataframe(results_df)
                    except Exception as db_error:
                        st.error(f"Database execution error: {db_error}")
                    finally:
                        conn.close() # Always close the cloud connection!

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question first.")