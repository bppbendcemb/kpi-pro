#!/usr/bin/env python
"""
Example: Using the Monthly KPI Report Sync Feature
ตัวอย่าง: การใช้งาน Monthly KPI Report Sync

This script demonstrates how to use the sync_monthly_kpi_report function
from Python code directly.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

# Now we can import from app modules
from services.sync_service import sync_monthly_kpi_report, validate_connection, get_sync_status

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def example_1_validate_connections():
    """Example 1: Validate database connections"""
    print_header("Example 1: Validate Database Connections")
    
    is_valid, msg = validate_connection()
    print(f"\nStatus: {'✓ VALID' if is_valid else '✗ INVALID'}")
    print(f"Message: {msg}\n")
    
    return is_valid

def example_2_sync_single_year():
    """Example 2: Sync monthly KPI report for a single year"""
    print_header("Example 2: Sync Monthly KPI Report (2025)")
    
    print("Executing: EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025")
    print("\nProcessing...")
    
    rows, error = sync_monthly_kpi_report(year=2025)
    
    if error is None:
        print(f"\n✓ SUCCESS: Synced {rows} rows")
        print(f"  - Data saved to: PostgreSQL public.data table")
        print(f"  - Year: 2025")
        print(f"  - Rows: {rows}")
    else:
        print(f"\n✗ ERROR: {error}")
    
    return rows if error is None else 0

def example_3_sync_multiple_years():
    """Example 3: Sync multiple years"""
    print_header("Example 3: Sync Multiple Years")
    
    years = [2023, 2024, 2025]
    total_rows = 0
    
    for year in years:
        print(f"\nSyncing year {year}...")
        rows, error = sync_monthly_kpi_report(year=year)
        
        if error is None:
            print(f"  ✓ Year {year}: {rows} rows synced")
            total_rows += rows
        else:
            print(f"  ✗ Year {year}: {error}")
    
    print(f"\n{'='*70}")
    print(f"Total rows synced: {total_rows}")
    print(f"{'='*70}\n")
    
    return total_rows

def example_4_check_sync_status():
    """Example 4: Check current sync status"""
    print_header("Example 4: Check Synchronization Status")
    
    status = get_sync_status()
    
    print(f"\nStatus: {status.get('status', 'unknown')}")
    
    if 'tables' in status:
        print("\nTable Status:")
        print("-" * 70)
        print(f"{'Table':<25} {'Rows':<15} {'Status':<10}")
        print("-" * 70)
        
        for table in status['tables']:
            print(f"{table['table']:<25} {table['rows']:<15} {table['status']:<10}")
        
        print("-" * 70)
        print(f"Total tables: {status.get('total_tables', 0)}\n")

def example_5_error_handling():
    """Example 5: Proper error handling"""
    print_header("Example 5: Error Handling")
    
    print("Attempting to sync with invalid year...")
    
    # This should work but might return 0 rows if no data exists
    rows, error = sync_monthly_kpi_report(year=9999)
    
    if error is not None:
        print(f"Error occurred: {error}")
    else:
        if rows == 0:
            print("✓ Sync completed (0 rows found)")
        else:
            print(f"✓ Sync completed ({rows} rows synced)")
    
    print()

def main():
    """Run examples"""
    print("\n" + "="*70)
    print("  Monthly KPI Report Sync - Usage Examples")
    print("="*70)
    
    try:
        # Example 1: Validate connections
        if not example_1_validate_connections():
            print("⚠️  Database connections are not valid!")
            print("   Please check your environment configuration.")
            return 1
        
        # Example 2: Sync single year
        print("\nProceeding with sync examples...")
        input("Press Enter to continue (Example 2)...")
        example_2_sync_single_year()
        
        # Example 3: Sync multiple years (optional)
        print("\n" + "="*70)
        response = input("Run Example 3 (sync multiple years)? (y/n): ").strip().lower()
        if response == 'y':
            input("Press Enter to continue...")
            example_3_sync_multiple_years()
        
        # Example 4: Check status
        print("\n" + "="*70)
        response = input("Run Example 4 (check status)? (y/n): ").strip().lower()
        if response == 'y':
            input("Press Enter to continue...")
            example_4_check_sync_status()
        
        # Example 5: Error handling
        print("\n" + "="*70)
        response = input("Run Example 5 (error handling)? (y/n): ").strip().lower()
        if response == 'y':
            input("Press Enter to continue...")
            example_5_error_handling()
        
        print("\n" + "="*70)
        print("  Examples completed!")
        print("="*70 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
