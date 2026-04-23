# Quick Start Guide - Monthly KPI Report Sync

## 🚀 Quick Start

### Option 1: Using the API (HTTP Request)

```bash
# Sync monthly KPI report for 2025
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'
```

### Option 2: Using CLI

```bash
# Navigate to app directory
cd app

# Sync monthly KPI report for 2025
python cli_sync.py --sync-kpi --year 2025

# Sync for a different year
python cli_sync.py --sync-kpi --year 2024
```

### Option 3: Using Python Code

```python
import sys
sys.path.insert(0, 'app')

from services.sync_service import sync_monthly_kpi_report

rows, error = sync_monthly_kpi_report(year=2025)
if error:
    print(f"Error: {error}")
else:
    print(f"Success! Synced {rows} rows")
```

## 📊 What It Does

```
MSSQL (hrmbppSQL)
    ↓
EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025
    ↓
PostgreSQL (public.data table)
```

## 🔧 Docker Compose

If using Docker:

```bash
# Start services
docker-compose up -d

# Wait a few seconds for services to start

# Run sync via API
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'
```

## ✅ Verify It Worked

### Check API Response

```bash
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'

# Look for "status": "success" in response
```

### Check PostgreSQL

```bash
# Access PostgreSQL
psql -h localhost -U admincomp -d kpidb

# List data
SELECT COUNT(*) FROM public.data;
SELECT * FROM public.data LIMIT 5;

# Check year filter
SELECT DISTINCT year FROM public.data ORDER BY year DESC;
```

### Check Logs

```bash
# View logs
tail -f /app/logs/sync_service.log

# Or with Docker
docker logs kpi-pro_app_1 -f
```

## 📝 API Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/sync/monthly-kpi` | Execute stored procedure & sync |
| POST | `/sync` | Sync all tables (existing) |
| GET | `/api/status` | Check synchronization status |
| GET | `/api/health` | Health check |

## 🛠️ CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `--sync-kpi --year 2025` | Sync monthly KPI for 2025 |
| `--sync-all` | Sync all tables |
| `--status` | Check sync status |
| `--validate` | Test database connections |

## 🔍 Troubleshooting

### No data returned?
```bash
# Check if stored procedure exists in MSSQL
SELECT * FROM sys.procedures WHERE name = 'sp_GetMonthlyKPIReport'

# Check if public.data table exists in PostgreSQL
SELECT * FROM information_schema.tables WHERE table_schema='public'
```

### Connection failed?
```bash
# Validate connections
python app/cli_sync.py --validate

# Check environment variables
cat .env | grep MSSQL
cat .env | grep POSTGRES
```

### Check detailed logs
```bash
tail -100 /app/logs/sync_service.log
```

## 📦 Files Modified/Created

- ✅ `app/services/sync_service.py` - Added `sync_monthly_kpi_report()` function
- ✅ `app/routes/data_routes.py` - Added `/api/sync/monthly-kpi` endpoint
- ✅ `app/cli_sync.py` - New CLI tool
- ✅ `MONTHLY_KPI_SYNC.md` - Full documentation

## 💡 Next Steps

1. ✅ Run the sync: `python app/cli_sync.py --sync-kpi --year 2025`
2. ✅ Verify in PostgreSQL: `SELECT COUNT(*) FROM public.data;`
3. ✅ View logs: `tail -f /app/logs/sync_service.log`
4. ✅ Set up scheduled sync (cron job or scheduled task)

## 📚 See Also

- [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md) - Full documentation
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- [QUICKSTART.md](QUICKSTART.md) - General quick start
