from dotenv import load_dotenv
import os
import mysql.connector

# Load .env from the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
print(get_db_connection())
