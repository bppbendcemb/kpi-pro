import os
from sqlalchemy import create_engine
import pymssql

# สำหรับ PostgreSQL (ปลายทาง)
def get_pg_engine():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    db = os.getenv('POSTGRES_DB')
    port = os.getenv('POSTGRES_PORT', '5432')
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

# สำหรับ SQL Server (ต้นทาง)
def get_mssql_conn(database=None):
    if database is None:
        database = os.getenv('MSSQL_DB')
        
    return pymssql.connect(
        server=os.getenv('MSSQL_HOST'),
        user=os.getenv('MSSQL_USER'),
        password=os.getenv('MSSQL_PASS'),
        database=database
    )