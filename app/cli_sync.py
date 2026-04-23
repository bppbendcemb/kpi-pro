#!/usr/bin/env python
"""
Command-line interface for KPI data synchronization
ส่วนติดต่อบรรทัดคำสั่งสำหรับการซิงค์ข้อมูล KPI
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.sync_service import (
    sync_kpi_data,
    sync_monthly_kpi_report,
    validate_connection,
    get_sync_status
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description='KPI Pro Data Synchronization CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_sync.py --sync-all              # Sync all tables from MSSQL to PostgreSQL
  python cli_sync.py --sync-kpi --year 2025 # Sync monthly KPI report for 2025
  python cli_sync.py --status                # Check sync status
  python cli_sync.py --validate              # Validate database connections
        """
    )
    
    # Add arguments
    parser.add_argument(
        '--sync-all',
        action='store_true',
        help='Sync all KPI tables from MSSQL to PostgreSQL'
    )
    
    parser.add_argument(
        '--sync-kpi',
        action='store_true',
        help='Execute MSSQL stored procedure sp_GetMonthlyKPIReport and save to PostgreSQL'
    )
    
    parser.add_argument(
        '--year',
        type=int,
        default=2025,
        help='Year for monthly KPI report (default: 2025)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Get current synchronization status'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate database connections'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.validate:
        logger.info("Validating database connections...")
        is_valid, msg = validate_connection()
        print(msg)
        return 0 if is_valid else 1
    
    elif args.status:
        logger.info("Getting synchronization status...")
        status = get_sync_status()
        print(f"\n{'='*60}")
        print(f"Sync Status: {status.get('status', 'unknown')}")
        if 'tables' in status:
            print(f"{'='*60}")
            for table in status['tables']:
                print(f"  {table['table']:<20} {table['rows']:>10} rows  [{table['status']}]")
        print(f"{'='*60}\n")
        return 0
    
    elif args.sync_all:
        logger.info("Starting full data synchronization...")
        rows, error = sync_kpi_data()
        if error:
            logger.error(f"Sync failed: {error}")
            return 1
        else:
            logger.info(f"Sync completed successfully: {rows} rows synchronized")
            return 0
    
    elif args.sync_kpi:
        logger.info(f"Starting monthly KPI report sync for year {args.year}...")
        rows, error = sync_monthly_kpi_report(year=args.year)
        if error:
            logger.error(f"Monthly KPI sync failed: {error}")
            return 1
        else:
            logger.info(f"Monthly KPI sync completed: {rows} rows synchronized")
            return 0
    
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
