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
You are an expert PostgreSQL translator. 

CRITICAL RULE: 
- PostgreSQL is case-sensitive. Always wrap table names and column names in double quotes exactly as shown below (e.g., SELECT * FROM "Students").
- Use single quotes (') for data values (e.g., WHERE "major" = 'Computer Science').

Table: "Students"
Columns: "student_id", "name", "major", "enrollment_year"

Table: "Courses"
Columns: "course_id", "course_name", "department", "credits"

Table: "Enrollments"
Columns: "enrollment_id", "student_id", "course_id", "grade"
"""
def get_sql_from_ai(user_question):
    """Sends the user's question and our schema to Gemini to get a SQL query."""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    prompt = SCHEMA_PROMPT + f"\n\nUser Question: {user_question}\nSQL Query:"
    response = model.generate_content(prompt)

    return response.text.strip()

# 3. Streamlit Frontend UI
st.set_page_config(page_title="TalkDB", page_icon="🗄️")
st.title("TalkDB: Natural Language to PostgreSQL Interface")
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