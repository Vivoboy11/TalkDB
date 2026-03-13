import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_query(sql_query):
    """
    Executes a raw SQL query on your Supabase PostgreSQL database 
    and returns a Pandas DataFrame.
    """
    db_url = os.environ.get("DATABASE_URL")
    conn = None
    
    try:
        # Connect to Supabase
        # Connect with a timeout to prevent hanging
        conn = psycopg2.connect(db_url, connect_timeout=10)
        
        # We use pandas here because Streamlit renders DataFrames beautifully
        df = pd.read_sql_query(sql_query, conn)
        return df
        
    except Exception as e:
        return f"Error executing query: {e}"
        
    finally:
        # Always close the cloud connection when done!
        if conn is not None:
            conn.close()

# Note: We removed the setup_database() function because your cloud 
# database is already set up and your data is stored safely on Supabase!