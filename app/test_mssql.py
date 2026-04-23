import os
import pymssql
from dotenv import load_dotenv

# Load .env file
load_dotenv()

host = os.getenv('MSSQL_HOST')
user = os.getenv('MSSQL_USER')
password = os.getenv('MSSQL_PASS')
database = os.getenv('MSSQL_DB_HRM') # Try HRM first

def test_conn(server_str, port=None, tds_version=None):
    print(f"Testing: {server_str} (Port: {port}, TDS: {tds_version})")
    try:
        conn = pymssql.connect(
            server=server_str,
            port=port,
            user=user,
            password=password,
            database=database,
            timeout=3,
            tds_version=tds_version
        )
        print(f"SUCCESS with {server_str}")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED with {server_str}: {e}")
        return False

# Try various formats
test_conn(host)
test_conn("10.11.0.2", tds_version='7.0')
test_conn("10.11.0.2", tds_version='7.4')
test_conn("10.11.0.2", port=1433)
test_conn("10.11.0.2", port=1434)


