
import os
from sqlalchemy import create_engine, text
import json

# Manual env set
os.environ['POSTGRES_USER'] = 'admincomp'
os.environ['POSTGRES_PASSWORD'] = "g-9[k'[vo"
os.environ['POSTGRES_DB'] = 'kpidb'
os.environ['POSTGRES_PORT'] = '5432'
os.environ['POSTGRES_HOST'] = 'localhost' # Try localhost first

def get_pg_engine():
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    db = os.environ['POSTGRES_DB']
    port = os.environ['POSTGRES_PORT']
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

try:
    engine = get_pg_engine()
    with engine.connect() as conn:
        # Check units
        result = conn.execute(text("SELECT DISTINCT unit FROM public.activities"))
        units = [row[0] for row in result]
        print(f"Units found: {units}")

        # Check some data
        result = conn.execute(text("SELECT kpi_id, unit, activities FROM public.activities LIMIT 20"))
        samples = [dict(row._mapping) for row in result]
        print(f"Samples: {json.dumps(samples, indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
