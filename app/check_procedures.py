import os
import pymssql
from dotenv import load_dotenv

# Load .env file
load_dotenv()

host = os.getenv('MSSQL_HOST')
user = os.getenv('MSSQL_USER')
password = os.getenv('MSSQL_PASS')
db_hrm = os.getenv('MSSQL_DB_HRM')
db_it = os.getenv('MSSQL_DB_IT')

def list_procedures(db_name):
    print(f"\nListing procedures in {db_name}...")
    try:
        conn = pymssql.connect(
            server=host,
            user=user,
            password=password,
            database=db_name,
            timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.procedures ORDER BY name")
        procedures = cursor.fetchall()
        if not procedures:
            print("  No procedures found.")
        for proc in procedures:
            print(f"  - {proc[0]}")
        conn.close()
    except Exception as e:
        print(f"  Error: {e}")

list_procedures(db_hrm)
list_procedures(db_it)
