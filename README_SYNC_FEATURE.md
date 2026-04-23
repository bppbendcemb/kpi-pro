# Monthly KPI Report Sync - Complete Implementation

## 📋 Overview

This implementation enables executing the MSSQL stored procedure **`sp_GetMonthlyKPIReport`** and automatically syncing results to PostgreSQL.

**SQL Query:**
```sql
EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025;
```

**Thai Translation:**
```
ดึงข้อมูล KPI รายเดือนจาก MSSQL มาบันทึกลง PostgreSQL
```

---

## 🎯 What This Does

```
┌──────────────────────────────────────────────────────────────┐
│ MSSQL Server (hrmbppSQL Database)                            │
│ Stored Procedure: [dbo].[sp_GetMonthlyKPIReport]             │
│ Parameter: @yr = 2025                                         │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ↓ EXEC with year parameter
                     
┌──────────────────────────────────────────────────────────────┐
│ Python Data Processing                                        │
│ - Fetch all results                                            │
│ - Convert to DataFrame                                        │
│ - Batch process (1000 rows/batch)                            │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ↓ Save via SQLAlchemy
                     
┌──────────────────────────────────────────────────────────────┐
│ PostgreSQL Database (kpidb)                                  │
│ Table: public.data                                            │
│ All monthly KPI data synced and ready for querying            │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 What Was Implemented

### 1. **Core Service Function**
   - **File:** `app/services/sync_service.py`
   - **Function:** `sync_monthly_kpi_report(year: int = 2025)`
   - **What it does:**
     - Connects to MSSQL Server
     - Executes the stored procedure
     - Retrieves all results
     - Saves to PostgreSQL `public.data` table
     - Returns success/error status

### 2. **REST API Endpoint**
   - **File:** `app/routes/data_routes.py`
   - **Endpoint:** `POST /api/sync/monthly-kpi`
   - **What it does:**
     - Accepts year as JSON parameter
     - Calls the sync service
     - Returns JSON response with status

### 3. **Command-Line Interface**
   - **File:** `app/cli_sync.py`
   - **Command:** `python cli_sync.py --sync-kpi --year 2025`
   - **What it does:**
     - Provides CLI interface to sync data
     - Supports multiple commands (sync, validate, status)
     - Full logging and error reporting

### 4. **Documentation** (3 files)
   - `MONTHLY_KPI_SYNC.md` - Complete technical documentation
   - `MONTHLY_KPI_QUICK_START.md` - Quick start guide
   - `IMPLEMENTATION_SUMMARY.md` - Implementation overview

### 5. **Example Script**
   - `example_usage.py` - Interactive examples of all features

---

## 🚀 Quick Start

### Option A: Via REST API

```bash
# Sync monthly KPI report for 2025
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'

# Expected Response:
{
  "status": "success",
  "year": 2025,
  "rows": 1234,
  "message": "Successfully synced 1234 rows from sp_GetMonthlyKPIReport"
}
```

### Option B: Via CLI

```bash
# Navigate to app directory
cd app

# Run the sync
python cli_sync.py --sync-kpi --year 2025

# Output:
# 2025-04-23 10:30:45,123 - __main__ - INFO - Starting monthly KPI report sync...
# 2025-04-23 10:30:46,456 - sync_service - INFO - ✓ Connected to MSSQL Server [hrmbppSQL]
# 2025-04-23 10:30:47,789 - sync_service - INFO - ✓ Retrieved 1234 rows from stored procedure
# 2025-04-23 10:30:48,234 - sync_service - INFO - ✓ Successfully saved 1234 rows to public.data
```

### Option C: Via Python Code

```python
from services.sync_service import sync_monthly_kpi_report

# Execute sync
rows, error = sync_monthly_kpi_report(year=2025)

# Check result
if error is None:
    print(f"Success! Synced {rows} rows")
else:
    print(f"Error: {error}")
```

### Option D: Run Interactive Examples

```bash
python example_usage.py
```

---

## 🔧 Configuration

### Required Environment Variables

Your `.env` file should contain:

```ini
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

**Verification:**
```bash
python app/cli_sync.py --validate
```

---

## 📊 Verifying Results

### Check via CLI

```bash
# Count rows synced
psql -h postgres-db -U admincomp -d kpidb \
  -c "SELECT COUNT(*) FROM public.data;"

# View sample data
psql -h postgres-db -U admincomp -d kpidb \
  -c "SELECT * FROM public.data LIMIT 5;"

# Check data by year
psql -h postgres-db -U admincomp -d kpidb \
  -c "SELECT year, COUNT(*) as rows FROM public.data GROUP BY year;"
```

### Check via Python

```python
import pandas as pd
from config.db_config import get_pg_engine

engine = get_pg_engine()
df = pd.read_sql("SELECT * FROM public.data", engine)
print(f"Total rows: {len(df)}")
print(df.head())
```

### Check Logs

```bash
# View live logs
tail -f /app/logs/sync_service.log

# View with Docker
docker logs kpi-pro_app_1 -f
```

---

## 📚 File Structure

```
kpi-pro/
├── app/
│   ├── cli_sync.py                 # ✨ NEW: CLI tool
│   ├── services/
│   │   └── sync_service.py         # ✨ UPDATED: Added sync_monthly_kpi_report()
│   ├── routes/
│   │   └── data_routes.py          # ✨ UPDATED: Added /api/sync/monthly-kpi
│   └── config/
│       └── db_config.py            # (no changes needed)
│
├── MONTHLY_KPI_SYNC.md             # ✨ NEW: Full technical docs
├── MONTHLY_KPI_QUICK_START.md      # ✨ NEW: Quick start guide
├── IMPLEMENTATION_SUMMARY.md       # ✨ NEW: Implementation overview
├── example_usage.py                # ✨ NEW: Usage examples
└── .env                            # (existing config file)
```

---

## 🔌 API Reference

### Endpoint: Sync Monthly KPI Report

```http
POST /api/sync/monthly-kpi HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "year": 2025
}
```

**Response (Success - 200):**
```json
{
    "status": "success",
    "year": 2025,
    "rows": 1234,
    "message": "Successfully synced 1234 rows from sp_GetMonthlyKPIReport"
}
```

**Response (Error - 400/500):**
```json
{
    "status": "error",
    "year": 2025,
    "rows": 0,
    "error": "Connection failed: [error details]"
}
```

### Other Available Endpoints

- `POST /sync` - Sync all predefined tables
- `GET /api/status` - Get synchronization status
- `GET /api/health` - Health check

---

## 🛠️ CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `--sync-kpi --year 2025` | Sync monthly KPI report |
| `--sync-kpi --year 2024` | Sync for different year |
| `--sync-all` | Sync all predefined tables |
| `--status` | Show sync status |
| `--validate` | Test database connections |

**Examples:**
```bash
# Sync 2025 data
python cli_sync.py --sync-kpi --year 2025

# Check everything is working
python cli_sync.py --validate

# View current status
python cli_sync.py --status
```

---

## 🔍 Troubleshooting

### "Connection failed to MSSQL"
```bash
# Validate connections
python app/cli_sync.py --validate

# Check credentials
cat .env | grep MSSQL
```

### "PostgreSQL connection failed"
```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# Test connection manually
psql -h postgres-db -U admincomp -d kpidb -c "SELECT 1;"
```

### "Stored procedure not found"
```sql
-- In MSSQL, check if procedure exists
SELECT * FROM sys.procedures WHERE name = 'sp_GetMonthlyKPIReport'

-- View procedure definition
sp_helptext '[dbo].[sp_GetMonthlyKPIReport]'
```

### "No data returned"
```sql
-- Verify data exists for year in MSSQL
EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025
```

### View Detailed Logs
```bash
tail -100 /app/logs/sync_service.log
```

---

## 🚦 Testing the Implementation

### 1. Validate Setup
```bash
cd app
python cli_sync.py --validate
# Should see: ✓ All connections validated successfully
```

### 2. Test Sync (2025)
```bash
python cli_sync.py --sync-kpi --year 2025
# Should see: ✓ Successfully saved [N] rows to public.data
```

### 3. Verify Data
```bash
psql -h postgres-db -U admincomp -d kpidb
> SELECT COUNT(*) FROM public.data;
# Should return a number > 0
```

### 4. Test API
```bash
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'
```

---

## 🎓 Learning Resources

### Understand the Flow
1. Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for overview
2. Read [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md) for technical details
3. Run `python example_usage.py` for interactive examples

### Database Details
- MSSQL Docs: [sp_executesql](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-executesql-transact-sql)
- PostgreSQL Docs: [Using SQLAlchemy](https://docs.sqlalchemy.org/)

### Python Libraries Used
- `pymssql` - MSSQL Server connection
- `psycopg2` - PostgreSQL connection
- `pandas` - Data manipulation
- `sqlalchemy` - Database abstraction
- `python-dotenv` - Environment variables

---

## 📞 Support

### Quick Checklist
- [ ] Environment variables configured in `.env`
- [ ] MSSQL Server is accessible
- [ ] PostgreSQL Server is running
- [ ] Stored procedure exists in MSSQL
- [ ] Database credentials are correct
- [ ] Docker containers are running (if using Docker)

### Common Tasks

**Sync 2024 data:**
```bash
python app/cli_sync.py --sync-kpi --year 2024
```

**Sync multiple years at once:**
```bash
for year in 2023 2024 2025; do
  python app/cli_sync.py --sync-kpi --year $year
done
```

**Clear and resync:**
```bash
# Warning: This deletes all data in public.data
psql -h postgres-db -U admincomp -d kpidb -c "TRUNCATE TABLE public.data;"

# Then sync again
python app/cli_sync.py --sync-kpi --year 2025
```

---

## ✨ Features

✅ **Three interfaces:** API, CLI, Python code
✅ **Error handling:** Comprehensive error messages & logging
✅ **Performance:** Batch processing (1000 rows/batch)
✅ **Flexibility:** Support for multiple years
✅ **Monitoring:** Built-in status checking
✅ **Documentation:** Complete guides included
✅ **Examples:** Interactive usage examples
✅ **Logging:** Detailed logs for debugging

---

## 📅 Next Steps

1. **Test the implementation** - Run `python example_usage.py`
2. **Verify data** - Check PostgreSQL for synced data
3. **Schedule syncs** - Set up cron jobs for regular updates
4. **Monitor** - Watch logs for any issues
5. **Optimize** - Adjust batch size if needed

---

**Implementation Date:** April 23, 2025  
**Status:** ✅ Ready to use  
**Version:** 1.0.0
