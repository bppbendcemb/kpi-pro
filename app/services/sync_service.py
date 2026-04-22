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