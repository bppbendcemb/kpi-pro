# Monthly KPI Report Sync Implementation

## Overview

This implementation enables executing the MSSQL stored procedure `sp_GetMonthlyKPIReport` and synchronizing the results to PostgreSQL's `public.data` table.

**SQL Command:**
```sql
EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025;
```

## Components

### 1. **Sync Service Function** (`app/services/sync_service.py`)

**Function:** `sync_monthly_kpi_report(year: int = 2025)`

- Connects to MSSQL Server
- Executes the stored procedure with specified year
- Fetches results and converts to DataFrame
- Saves data to PostgreSQL `public.data` table
- Returns: `(rows_synced: int, error: Optional[str])`

**Features:**
- Comprehensive error handling
- Detailed logging
- Automatic connection cleanup
- Batch processing for large datasets

### 2. **API Endpoint** (`app/routes/data_routes.py`)

**Endpoint:** `POST /api/sync/monthly-kpi`

**Request Body:**
```json
{
    "year": 2025
}
```

**Response (Success):**
```json
{
    "status": "success",
    "year": 2025,
    "rows": 1234,
    "message": "Successfully synced 1234 rows from sp_GetMonthlyKPIReport"
}
```

**Response (Error):**
```json
{
    "status": "error",
    "year": 2025,
    "rows": 0,
    "error": "Error message details"
}
```

### 3. **CLI Interface** (`app/cli_sync.py`)

Command-line tool for executing sync operations.

## Usage Examples

### Via API (cURL)

```bash
# Sync monthly KPI report for 2025
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'

# Sync for 2024
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2024}'
```

### Via CLI

```bash
# Sync monthly KPI report for 2025
python app/cli_sync.py --sync-kpi --year 2025

# Sync for 2024
python app/cli_sync.py --sync-kpi --year 2024

# Check sync status
python app/cli_sync.py --status

# Validate connections
python app/cli_sync.py --validate

# Sync all tables (existing functionality)
python app/cli_sync.py --sync-all
```

### Via Python Code

```python
from services.sync_service import sync_monthly_kpi_report

# Execute sync
rows, error = sync_monthly_kpi_report(year=2025)

if error is None:
    print(f"Successfully synced {rows} rows")
else:
    print(f"Error: {error}")
```

## Database Schema

### MSSQL Side
- **Stored Procedure:** `[dbo].[sp_GetMonthlyKPIReport]`
- **Parameter:** `@yr` (integer, e.g., 2025)
- Database: itcomputer (from MSSQL_DB_IT env var)

### PostgreSQL Side
- **Table:** `public.data`
- **Schema:** `public`
- **Operation:** Data is appended to existing table (use `replace` mode to clear first)

## Configuration

### Environment Variables Required

```
# MSSQL Configuration
MSSQL_HOST=10.11.0.2\SQLEXPRESS
MSSQL_USER=bppnet
MSSQL_PASS=your_password
MSSQL_DB_HRM=hrmbppSQL

# PostgreSQL Configuration
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432
POSTGRES_USER=admincomp
POSTGRES_PASSWORD=your_password
POSTGRES_DB=kpidb
```

## Implementation Details

### Process Flow

1. **Connect to MSSQL**
   - Uses `get_mssql_conn()` from `config/db_config.py`
   - Connects to IT database

2. **Execute Stored Procedure**
   - Executes: `EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = {year}`
   - Fetches all rows and column names

3. **Data Processing**
   - Converts results to Pandas DataFrame
   - Maintains all columns from stored procedure output

4. **Save to PostgreSQL**
   - Uses SQLAlchemy for connection
   - Saves to `public.data` table
   - Uses batch insert (1000 rows per batch)
   - Mode: `append` (add to existing) or `replace` (clear first)

### Error Handling

The function handles:
- MSSQL connection failures
- Stored procedure execution errors
- PostgreSQL connection failures
- Data insertion errors
- Empty result sets
- Unexpected exceptions

All errors are logged with full traceback for debugging.

## Logging

Logs are written to:
- **File:** `/app/logs/sync_service.log`
- **Console:** Direct output

Log format: `timestamp - service - level - message`

## Data Flow Diagram

```
MSSQL Server
    ↓
[dbo].[sp_GetMonthlyKPIReport] @yr = 2025
    ↓
Python Service (pandas DataFrame)
    ↓
PostgreSQL
    ↓
public.data table
    ↓
API Response (JSON)
```

## Monitoring

### Check Sync Status
```bash
curl http://localhost:5000/api/status
```

### View Logs
```bash
# Real-time
tail -f /app/logs/sync_service.log

# Last 50 lines
tail -50 /app/logs/sync_service.log
```

## Troubleshooting

### Connection Issues

1. **MSSQL Connection Failed**
   - Verify MSSQL server is running
   - Check credentials in `.env`
   - Verify network connectivity to MSSQL host

2. **PostgreSQL Connection Failed**
   - Verify PostgreSQL is running
   - Check credentials in `.env`
   - Verify database exists

### Stored Procedure Issues

1. **Stored Procedure Not Found**
   - Verify procedure exists: `SELECT * FROM sys.procedures WHERE name = 'sp_GetMonthlyKPIReport'`
   - Check correct database is selected
   - Verify database owner/permissions

2. **No Data Returned**
   - Verify data exists for the specified year
   - Check stored procedure logic
   - Run procedure manually in MSSQL to verify

## Related Functions

- `sync_kpi_data()` - Sync all predefined tables
- `validate_connection()` - Test all database connections
- `get_sync_status()` - Get current status of all synced tables
- `get_mssql_conn()` - Create MSSQL connection
- `get_pg_engine()` - Create PostgreSQL engine

## File Modifications

Files modified/created for this implementation:
1. `app/services/sync_service.py` - Added `sync_monthly_kpi_report()` function
2. `app/routes/data_routes.py` - Added `/api/sync/monthly-kpi` endpoint
3. `app/cli_sync.py` - Created new CLI interface
4. `MONTHLY_KPI_SYNC.md` - This documentation file
