
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'app'))

from config.db_config import get_pg_engine
from sqlalchemy import text

os.environ['POSTGRES_USER'] = 'admincomp'
os.environ['POSTGRES_PASSWORD'] = "g-9[k'[vo"
os.environ['POSTGRES_DB'] = 'kpidb'
os.environ['POSTGRES_PORT'] = '5432'
os.environ['POSTGRES_HOST'] = 'localhost'

engine = get_pg_engine()
with engine.connect() as conn:
    # Check if goals table exists
    result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'goals')"))
    exists = result.scalar()
    print(f"Goals table exists: {exists}")

    if exists:
        result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'goals'"))
        columns = [f"{row[0]} ({row[1]})" for row in result]
        print(f"Columns: {columns}")
    else:
        # Create it based on the user's query context
        print("Creating goals table...")
        conn.execute(text("""
            CREATE TABLE public.goals (
                kpi_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                target NUMERIC(18, 2),
                PRIMARY KEY (kpi_id, year)
            )
        """))
        conn.commit()
        print("Goals table created.")
