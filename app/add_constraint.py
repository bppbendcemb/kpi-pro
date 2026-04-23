from config.db_config import get_pg_engine
from sqlalchemy import text

def add_constraint():
    engine = get_pg_engine()
    try:
        with engine.connect() as conn:
            # First, clean up duplicates if any
            print("Cleaning up duplicates...")
            conn.execute(text("""
                DELETE FROM public.data a USING public.data b
                WHERE a.data_id < b.data_id 
                AND a.kpi_id = b.kpi_id 
                AND a.year = b.year 
                AND a.month = b.month
            """))
            
            print("Adding unique constraint...")
            conn.execute(text("ALTER TABLE public.data ADD CONSTRAINT unique_kpi_year_month UNIQUE (kpi_id, year, month)"))
            conn.commit()
            print("✅ Constraint added successfully")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_constraint()
