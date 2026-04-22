import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

def init_database():
    """
    Initialize PostgreSQL database and create tables from CSV files in the 'data' folder
    Special handling for data_id, caldata_id, and id (goals) to be auto-increment keys.
    """
    print("🚀 Starting Database Initialization...")

    # DB Config
    user = os.getenv('POSTGRES_USER', 'appuser')
    password = os.getenv('POSTGRES_PASSWORD', 'apppassword')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    db_name = os.getenv('POSTGRES_DB', 'kpidb')

    # Connection string for 'postgres' default database
    postgres_url = f'postgresql://{user}:{password}@{host}:{port}/postgres'
    
    try:
        # 1. Create the database if it doesn't exist
        print(f"📡 Connecting to PostgreSQL at {host}:{port}...")
        engine_postgres = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
        
        with engine_postgres.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            exists = result.fetchone()
            
            if not exists:
                print(f"💎 Creating database '{db_name}'...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"✅ Database '{db_name}' created successfully.")
            else:
                print(f"ℹ️ Database '{db_name}' already exists.")
        
        engine_postgres.dispose()

        # 2. Connect to the target database
        target_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        engine = create_engine(target_url)
        print(f"🔗 Connected to database '{db_name}'.")

        # 3. Process each CSV in data/
        data_dir = 'data'
        if not os.path.exists(data_dir):
            print(f"❌ Error: Data directory '{data_dir}' not found.")
            return

        csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.csv')])
        print(f"📂 Found {len(csv_files)} CSV files. Importing tables...")

        for filename in csv_files:
            table_name = filename[:-4]
            file_path = os.path.join(data_dir, filename)
            
            print(f"⏳ Processing {filename} -> Table: {table_name}...")
            try:
                # Read CSV with encoding support
                try:
                    df = pd.read_csv(file_path)
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(file_path, encoding='tis-620')
                    except UnicodeDecodeError:
                        df = pd.read_csv(file_path, encoding='cp874')
                
                # Special Handling for Auto-increment keys
                if table_name == 'data':
                    if 'data_id' in df.columns:
                        df = df.drop(columns=['data_id'])
                    with engine.connect() as conn:
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                        conn.execute(text(f"""
                            CREATE TABLE {table_name} (
                                data_id SERIAL PRIMARY KEY,
                                kpi_id INTEGER,
                                year INTEGER,
                                month INTEGER,
                                value NUMERIC
                            )
                        """))
                        conn.commit()
                    df.to_sql(table_name, engine, if_exists='append', index=False)
                    
                elif table_name == 'caldata':
                    if 'caldata_id' in df.columns:
                        df = df.drop(columns=['caldata_id'])
                    with engine.connect() as conn:
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                        conn.execute(text(f"""
                            CREATE TABLE {table_name} (
                                caldata_id SERIAL PRIMARY KEY,
                                kpi_id INTEGER,
                                year INTEGER,
                                month INTEGER,
                                value NUMERIC,
                                note TEXT
                            )
                        """))
                        conn.commit()
                    df.to_sql(table_name, engine, if_exists='append', index=False)

                elif table_name == 'goals':
                    # Special handling for goals (id column)
                    if 'id' in df.columns:
                        df = df.drop(columns=['id'])
                    with engine.connect() as conn:
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                        conn.execute(text(f"""
                            CREATE TABLE {table_name} (
                                id SERIAL PRIMARY KEY,
                                kpi_id INTEGER,
                                year INTEGER,
                                target NUMERIC
                            )
                        """))
                        conn.commit()
                    df.to_sql(table_name, engine, if_exists='append', index=False)
                
                else:
                    # Default handling for other tables
                    df.to_sql(table_name, engine, if_exists='replace', index=False)
                
                print(f"   ✅ Successfully imported {len(df)} rows into '{table_name}'.")
            except Exception as e:
                print(f"   ❌ Error importing {filename}: {e}")

        print("\n✨ Database initialization complete!")
        print("=" * 40)

    except Exception as e:
        print(f"💥 Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
