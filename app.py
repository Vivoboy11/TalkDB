import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import database # Importing your newly upgraded database.py file!

# Load secrets from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. The System Prompt: Strict PostgreSQL Rules
SCHEMA_PROMPT = """
You are an expert PostgreSQL database administrator and SQL translator. Your job is to translate plain English into SQL queries for a PostgreSQL database.

CRITICAL RULE: You MUST write valid PostgreSQL syntax. Do NOT use SQLite syntax. 
- Use single quotes (') for strings, never double quotes (").
- Never use SQLite-specific functions.

Here is the schema of the database:

Table: Students
Columns: student_id (INTEGER PRIMARY KEY), name (TEXT), major (TEXT), enrollment_year (INTEGER)

Table: Courses
Columns: course_id (INTEGER PRIMARY KEY), course_name (TEXT), department (TEXT), credits (INTEGER)

Table: Enrollments
Columns: enrollment_id (INTEGER PRIMARY KEY), student_id (INTEGER, FOREIGN KEY), course_id (INTEGER, FOREIGN KEY), grade (TEXT)

Rules:
1. Output ONLY the raw SQL query. No markdown formatting (do not use ```sql), no explanations.
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
st.write("Ask a question in plain English, and the AI will query your cloud database.")

# Text input for the user
user_input = st.text_input("What would you like to know? (e.g., 'Show me all students in Computer Science')")

if st.button("Query Database"):
    if user_input:
        with st.spinner("Translating to SQL and fetching from Supabase..."):
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
                    # Run the query against our PostgreSQL database using the function from database.py
                    results = database.run_query(sql_query)
                    
                    # Display the results
                    if isinstance(results, str): # If our function returned an error string
                        st.error(results)
                    elif results.empty:
                        st.warning("Query ran successfully, but no results were found.")
                    else:
                        st.success("Results fetched successfully from the cloud!")
                        st.dataframe(results) 
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question first.")