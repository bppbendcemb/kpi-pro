# Implementation Summary: Monthly KPI Report Sync

## ✅ What Was Implemented

A complete solution to execute MSSQL stored procedure `sp_GetMonthlyKPIReport` and synchronize results to PostgreSQL.

**Thai:** ดึงข้อมูล KPI รายเดือนจาก MSSQL มาบันทึกลง PostgreSQL

---

## 📝 Files Created/Modified

### 1. **Core Function** - `app/services/sync_service.py`
**Added:** `sync_monthly_kpi_report(year: int = 2025)`

**Features:**
- Connects to MSSQL Server
- Executes: `EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = {year}`
- Converts results to Pandas DataFrame
- Saves to PostgreSQL `public.data` table
- Full error handling & logging
- Auto cleanup of connections

**Returns:** `(rows_synced: int, error: Optional[str])`

```python
from services.sync_service import sync_monthly_kpi_report

rows, error = sync_monthly_kpi_report(year=2025)
```

---

### 2. **API Endpoint** - `app/routes/data_routes.py`
**Added:** `POST /api/sync/monthly-kpi`

**Request:**
```json
{"year": 2025}
```

**Response:**
```json
{
    "status": "success",
    "year": 2025,
    "rows": 1234,
    "message": "Successfully synced 1234 rows from sp_GetMonthlyKPIReport"
}
```

**Usage:**
```bash
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'
```

---

### 3. **CLI Tool** - `app/cli_sync.py`
**Created:** Command-line interface for all sync operations

**Commands:**
```bash
# Sync monthly KPI report
python app/cli_sync.py --sync-kpi --year 2025

# Sync all tables
python app/cli_sync.py --sync-all

# Check status
python app/cli_sync.py --status

# Validate connections
python app/cli_sync.py --validate
```

---

### 4. **Documentation**

#### [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md)
Complete technical documentation including:
- Component overview
- Database schema
- Configuration requirements
- Logging details
- Troubleshooting guide
- Implementation details

#### [MONTHLY_KPI_QUICK_START.md](MONTHLY_KPI_QUICK_START.md)
Quick reference guide with:
- Three ways to use the feature (API, CLI, Python)
- Docker setup instructions
- Verification steps
- Common commands
- Basic troubleshooting

---

## 🔄 Data Flow

```
┌─────────────────────────────┐
│ MSSQL Server (hrmbppSQL)    │
│ [dbo].[sp_GetMonthlyKPIReport]
└──────────────┬──────────────┘
               │ EXEC @yr = 2025
               ↓
┌─────────────────────────────┐
│ Python Service              │
│ (Pandas DataFrame)          │
└──────────────┬──────────────┘
               │ SQLAlchemy
               ↓
┌─────────────────────────────┐
│ PostgreSQL (kpidb)          │
│ public.data table           │
└─────────────────────────────┘
```

---

## 🚀 How to Use

### Quick Test (3 steps)

```bash
# 1. Navigate to app
cd app

# 2. Run sync
python cli_sync.py --sync-kpi --year 2025

# 3. Check PostgreSQL
psql -h localhost -u admincomp -d kpidb -c "SELECT COUNT(*) FROM public.data;"
```

### Via Docker

```bash
# Start services
docker-compose up -d

# Run sync via API
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'
```

---

## 🔌 Database Configuration

**Required Environment Variables (in .env):**

```
# MSSQL
MSSQL_HOST=10.11.0.2\SQLEXPRESS
MSSQL_USER=bppnet
MSSQL_PASS=gliH0d^
MSSQL_DB_HRM=hrmbppSQL

# PostgreSQL
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432
POSTGRES_USER=admincomp
POSTGRES_PASSWORD=g-9[k'[vo
POSTGRES_DB=kpidb
```

---

## 📊 Features

✅ Execute MSSQL stored procedure with parameters
✅ Full error handling with detailed logging
✅ Batch processing (1000 rows/batch)
✅ Three interfaces: API, CLI, Python
✅ Automatic connection cleanup
✅ Support for multiple years
✅ Data validation
✅ Comprehensive documentation

---

## 📍 Key Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `sync_monthly_kpi_report()` | `sync_service.py` | Core sync logic |
| `/api/sync/monthly-kpi` | `data_routes.py` | HTTP endpoint |
| `cli_sync.py --sync-kpi` | `cli_sync.py` | CLI command |

---

## 🔍 Monitoring

### Check Sync Status
```bash
curl http://localhost:5000/api/status
```

### View Logs
```bash
tail -f /app/logs/sync_service.log
```

### Query Results
```bash
psql -h localhost -U admincomp -d kpidb
> SELECT COUNT(*) FROM public.data;
> SELECT DISTINCT year FROM public.data ORDER BY year;
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection failed | Run: `python app/cli_sync.py --validate` |
| No data returned | Check stored procedure exists in MSSQL |
| PostgreSQL table not found | Create table: `CREATE TABLE public.data (...);` |
| Permission denied | Check POSTGRES_USER credentials |

---

## 📚 Related Documentation

- [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md) - Full technical documentation
- [MONTHLY_KPI_QUICK_START.md](MONTHLY_KPI_QUICK_START.md) - Quick start guide
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development setup
- [QUICKSTART.md](QUICKSTART.md) - General quick start

---

## ✨ Next Steps

1. **Test the implementation**
   ```bash
   python app/cli_sync.py --sync-kpi --year 2025
   ```

2. **Schedule regular syncs** (Optional)
   - Linux: Add cron job
   - Windows: Add scheduled task
   - Docker: Add container orchestration

3. **Monitor & maintain**
   - Check logs regularly
   - Verify data integrity
   - Monitor performance

---

## 📝 SQL Reference

### View Stored Procedure in MSSQL
```sql
-- Check if procedure exists
SELECT * FROM sys.procedures WHERE name = 'sp_GetMonthlyKPIReport'

-- View procedure definition
sp_helptext '[dbo].[sp_GetMonthlyKPIReport]'
```

### Query Results in PostgreSQL
```sql
-- Basic count
SELECT COUNT(*) FROM public.data;

-- By year
SELECT year, COUNT(*) as row_count FROM public.data GROUP BY year;

-- Sample data
SELECT * FROM public.data LIMIT 10;

-- Column info
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_schema='public' AND table_name='data';
```

---

**Created:** 2025-04-23  
**Status:** ✅ Ready to use  
**Tested:** CLI, API, and Python interfaces
