"""
KPI Data Synchronization Service
Handles syncing multiple tables from different SQL Server databases to PostgreSQL
"""

import os
import pandas as pd
import logging
from datetime import datetime
from typing import Tuple, Optional
from sqlalchemy import text
from config.db_config import get_pg_engine, get_mssql_conn
from pathlib import Path

# Ensure logs directory exists
logs_dir = Path('/app/logs')
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/sync_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
# Mapping of Source Table to Destination Table and Source Database
# Adjust 'db' values based on where each table is located
TABLES_TO_SYNC = [
    {"source": "Activities", "dest": "activities", "db": os.getenv('MSSQL_DB_HRM')},
    {"source": "CalData", "dest": "caldata", "db": os.getenv('MSSQL_DB_HRM')},
    {"source": "Data", "dest": "kpi", "db": os.getenv('MSSQL_DB_HRM')},
    {"source": "Department", "dest": "department", "db": os.getenv('MSSQL_DB_HRM')},
    {"source": "Goals", "dest": "goals", "db": os.getenv('MSSQL_DB_HRM')},
    {"source": "Group_Table", "dest": "group", "db": os.getenv('MSSQL_DB_HRM')},
    # Example for IT database:
    # {"source": "ComputerAsset", "dest": "it_assets", "db": os.getenv('MSSQL_DB_IT')},
]
BATCH_SIZE = 1000


def sync_kpi_data() -> Tuple[int, Optional[str]]:
    """
    Synchronize all KPI-related tables from multiple SQL Server databases to PostgreSQL
    
    Returns:
        Tuple[int, Optional[str]]: (total rows synced, error message or None)
    """
    engine_pg = None
    total_synced = 0
    
    try:
        logger.info("=" * 60)
        logger.info("Starting Multi-Table Multi-DB KPI Data Synchronization")
        
        # Step 1: Connect to PostgreSQL (Destination)
        try:
            engine_pg = get_pg_engine()
            logger.info("✓ Successfully connected to PostgreSQL")
        except Exception as e:
            error_msg = f"PostgreSQL connection failed: {str(e)}"
            logger.error(error_msg)
            return 0, error_msg

        # Step 2: Loop through each table and sync
        for table_map in TABLES_TO_SYNC:
            src = table_map["source"]
            dst = table_map["dest"]
            db = table_map["db"]
            
            logger.info("-" * 40)
            logger.info(f"Processing Table: [{db}].[{src}] -> {dst}")
            
            conn_ms = None
            try:
                # Connect to specific SQL Server database
                conn_ms = get_mssql_conn(database=db)
                
                # Fetch data
                query = f"SELECT * FROM {src}"
                df = pd.read_sql(query, conn_ms)
                
                if len(df) == 0:
                    logger.warning(f"  ⚠ No data found in source table '{src}' in database '{db}'")
                    continue
                
                # Validation & Cleaning
                initial_rows = len(df)
                df = df.drop_duplicates()
                
                # Write to destination
                df.to_sql(
                    dst,
                    engine_pg,
                    if_exists='replace',
                    index=False,
                    chunksize=BATCH_SIZE,
                    method='multi'
                )
                
                rows_synced = len(df)
                total_synced += rows_synced
                logger.info(f"  ✓ Synced {rows_synced} rows (Duplicates removed: {initial_rows - rows_synced})")
                
            except Exception as e:
                logger.error(f"  ✗ Failed to sync table {src} from {db}: {str(e)}")
                continue
            finally:
                if conn_ms:
                    conn_ms.close()

        # Success
        logger.info("=" * 60)
        logger.info(f"✓ All synchronizations completed!")
        logger.info(f"  Total rows synchronized: {total_synced}")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        return total_synced, None
        
    except Exception as e:
        error_msg = f"Unexpected error during synchronization: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return 0, error_msg
    
    finally:
        if engine_pg:
            engine_pg.dispose()


def get_sync_status() -> dict:
    """
    Get current synchronization status for all tables
    """
    try:
        engine_pg = get_pg_engine()
        status_info = []
        
        with engine_pg.connect() as conn:
            for table_map in TABLES_TO_SYNC:
                dst = table_map["dest"]
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {dst}"))
                    row_count = result.scalar()
                    status_info.append({"table": dst, "rows": row_count, "status": "ok"})
                except Exception:
                    status_info.append({"table": dst, "rows": 0, "status": "missing"})
        
        return {
            "status": "healthy",
            "tables": status_info,
            "total_tables": len(status_info)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def validate_connection() -> Tuple[bool, str]:
    """
    Validate database connections
    """
    logger.info("Validating database connections...")
    
    # Test HRM database connection
    try:
        db_hrm = os.getenv('MSSQL_DB_HRM')
        conn = get_mssql_conn(database=db_hrm)
        conn.close()
        logger.info(f"✓ SQL Server [{db_hrm}] connection OK")
    except Exception as e:
        return False, f"✗ SQL Server HRM connection failed: {str(e)}"
    
    # Test IT database connection
    try:
        db_it = os.getenv('MSSQL_DB_IT')
        conn = get_mssql_conn(database=db_it)
        conn.close()
        logger.info(f"✓ SQL Server [{db_it}] connection OK")
    except Exception as e:
        return False, f"✗ SQL Server IT connection failed: {str(e)}"
    
    # Test PostgreSQL connection
    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ PostgreSQL connection OK")
    except Exception as e:
        return False, f"✗ PostgreSQL connection failed: {str(e)}"
    
    return True, "All connections validated successfully"


def sync_monthly_kpi_report(year: int = 2025) -> Tuple[int, Optional[str]]:
    """
    Execute MSSQL stored procedure sp_GetMonthlyKPIReport and save results to PostgreSQL
    ดึงข้อมูลรายเดือน KPI จาก MSSQL มาบันทึกลง PostgreSQL
    
    Args:
        year: The year to retrieve KPI data for (default: 2025)
    
    Returns:
        Tuple[int, Optional[str]]: (rows synced, error message or None)
    """
    engine_pg = None
    conn_ms = None
    cursor = None
    
    try:
        logger.info("=" * 60)
        logger.info(f"Starting Monthly KPI Report Sync (Year: {year})")
        
        # Step 1: Connect to MSSQL
        try:
            db = os.getenv('MSSQL_DB_IT')
            conn_ms = get_mssql_conn(database=db)
            logger.info(f"✓ Connected to MSSQL Server [{db}]")
        except Exception as e:
            error_msg = f"MSSQL connection failed: {str(e)}"
            logger.error(error_msg)
            return 0, error_msg
        
        # Step 2: Execute stored procedure
        try:
            # Create cursor and execute stored procedure
            cursor = conn_ms.cursor()
            logger.info(f"Executing: EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = {year}")
            cursor.execute(f"EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = {year}")
            
            # Fetch all results
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            if not rows:
                logger.warning(f"No data returned from stored procedure for year {year}")
                return 0, None
            
            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=columns)
            logger.info(f"✓ Retrieved {len(df)} rows from stored procedure")
            
            # Step 2.1: Filter columns to match PostgreSQL table schema
            # Required columns: kpi_id, year, month, value
            expected_columns = ['kpi_id', 'year', 'month', 'value']
            # Only keep columns that exist in the result and are expected in PG
            df = df[[col for col in expected_columns if col in df.columns]]
            
            # Step 2.2: Force numeric types to match PostgreSQL schema
            for col in ['kpi_id', 'year', 'month', 'value']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            logger.info(f"✓ Filtered and type-cast DataFrame columns: {df.columns.tolist()}")


            
        except Exception as e:
            error_msg = f"Failed to execute stored procedure: {str(e)}"
            logger.error(error_msg)
            return 0, error_msg
        finally:
            if cursor:
                cursor.close()
        
        # Step 3: Connect to PostgreSQL and save data
        try:
            engine_pg = get_pg_engine()
            logger.info("✓ Connected to PostgreSQL")
        except Exception as e:
            error_msg = f"PostgreSQL connection failed: {str(e)}"
            logger.error(error_msg)
            return 0, error_msg
        
        # Step 4: Save to public.data table with Upsert logic
        try:
            # We use a temporary table to perform the upsert (Insert or Update if exists)
            temp_table = f"temp_sync_{year}"
            
            with engine_pg.connect() as conn:
                # 1. Save DataFrame to temporary table
                df.to_sql(
                    temp_table,
                    engine_pg,
                    if_exists='replace',
                    index=False,
                    chunksize=BATCH_SIZE,
                    method='multi'
                )
                
                # 2. Perform the Upsert from temp table to main table
                # Based on kpi_id, year, month
                upsert_query = text(f"""
                    INSERT INTO public.data (kpi_id, year, month, value)
                    SELECT kpi_id, year, month, value FROM {temp_table}
                    ON CONFLICT (kpi_id, year, month) 
                    DO UPDATE SET 
                        value = EXCLUDED.value
                """)
                
                result = conn.execute(upsert_query)
                conn.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))
                conn.commit()
                
            rows_synced = len(df)
            logger.info(f"✓ Successfully upserted {rows_synced} rows to public.data")
            logger.info("=" * 60)
            
            return rows_synced, None

            
        except Exception as e:
            error_msg = f"Failed to save data to PostgreSQL: {str(e)}"
            logger.error(error_msg)
            return 0, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return 0, error_msg
    
    finally:
        # Cleanup connections
        if conn_ms:
            try:
                conn_ms.close()
            except Exception:
                pass
        if engine_pg:
            try:
                engine_pg.dispose()
            except Exception:
                pass