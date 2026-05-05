
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
    print("Adding unique constraint to goals table...")
    try:
        # First, check if there's already a primary key or unique constraint we can use
        # If not, add the composite unique constraint
        conn.execute(text("""
            ALTER TABLE public.goals 
            ADD CONSTRAINT unique_kpi_year UNIQUE (kpi_id, year);
        """))
        conn.commit()
        print("Constraint added successfully.")
    except Exception as e:
        print(f"Error adding constraint: {e}")
        conn.rollback()
        
        # Check current table structure
        result = conn.execute(text("""
            SELECT conname, contype 
            FROM pg_constraint 
            WHERE conrelid = 'public.goals'::regclass;
        """))
        print("Current constraints:")
        for row in result:
            print(row)
