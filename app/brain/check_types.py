from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = 'localhost'
db = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT', '5432')

safe_password = urllib.parse.quote_plus(password)
engine = create_engine(f'postgresql://{user}:{safe_password}@{host}:{port}/{db}')

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT active, istarget FROM public.activities LIMIT 1"))
        row = result.fetchone()
        if row:
            print(f"active type: {type(row[0])}, value: {row[0]}")
            print(f"istarget type: {type(row[1])}, value: {row[1]}")
        else:
            print("No data found")
except Exception as e:
    print(f"Error: {e}")
