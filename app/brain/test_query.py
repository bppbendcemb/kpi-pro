from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
db = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT', '5432')

# URL encode the password
safe_password = urllib.parse.quote_plus(password)

engine = create_engine(f'postgresql://{user}:{safe_password}@{host}:{port}/{db}')

try:
    with engine.connect() as conn:
        kpi_settings_query = text("""
            SELECT 
                k.kpi_id, 
                k.kpi_name, 
                a.group_id, 
                a.department_id, 
                a."no", 
                a.sub_no, 
                a.activities, 
                a.description, 
                a.description2, 
                a."source", 
                a."linkUrl", 
                a.unit, 
                a.source_result, 
                a.istarget, 
                a.active,
                d.department_desc,
                g.group_desc
            FROM public.kpis k
            LEFT JOIN public.activities a ON k.kpi_id = a.kpi_id
            LEFT JOIN public.department d ON a.department_id = d.department_id
            LEFT JOIN public."group" g ON a.group_id = g.group_id
            ORDER BY k.kpi_id
        """)
        result = conn.execute(kpi_settings_query)
        print(f"Success! Fetched {len(result.fetchall())} rows.")
except Exception as e:
    print(f"Error: {e}")
