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
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'activities'"))
        print("Columns in activities:")
        for row in result:
            print(f"- {row[0]}")
except Exception as e:
    print(f"Error: {e}")
