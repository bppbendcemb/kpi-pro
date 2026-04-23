# Getting Started Checklist

## ✅ Implementation Complete

Your monthly KPI report sync feature is now fully implemented and ready to use.

---

## 🎯 What You Can Do Now

Execute MSSQL stored procedure and sync to PostgreSQL:
```sql
EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025;
```

Three ways to use it:
1. **REST API** - HTTP POST request
2. **Command Line** - CLI tool
3. **Python Code** - Direct function call

---

## ⚡ 5-Minute Quick Start

### Step 1: Validate Setup (1 min)
```bash
cd app
python cli_sync.py --validate
```
✓ Should see: "All connections validated successfully"

### Step 2: Run Sync (1 min)
```bash
python cli_sync.py --sync-kpi --year 2025
```
✓ Should see: "Successfully saved [N] rows to public.data"

### Step 3: Verify Results (1 min)
```bash
psql -h postgres-db -U admincomp -d kpidb \
  -c "SELECT COUNT(*) FROM public.data;"
```
✓ Should return: A number > 0

### Step 4: Test API (1 min)
```bash
curl -X POST http://localhost:5000/api/sync/monthly-kpi \
  -H "Content-Type: application/json" \
  -d '{"year": 2025}'
```
✓ Should see JSON response with "status": "success"

### Step 5: Run Examples (1 min)
```bash
python example_usage.py
```
✓ Interactive examples showing all features

---

## 📁 Files Created/Modified

### New Files
- ✨ `app/cli_sync.py` - Command-line interface
- ✨ `MONTHLY_KPI_SYNC.md` - Full technical documentation  
- ✨ `MONTHLY_KPI_QUICK_START.md` - Quick reference
- ✨ `IMPLEMENTATION_SUMMARY.md` - Overview
- ✨ `README_SYNC_FEATURE.md` - Complete guide
- ✨ `example_usage.py` - Usage examples
- ✨ `GETTING_STARTED.md` - This file

### Updated Files
- 📝 `app/services/sync_service.py` - Added `sync_monthly_kpi_report()` function
- 📝 `app/routes/data_routes.py` - Added `/api/sync/monthly-kpi` endpoint

---

## 🔧 Configuration Check

Verify `.env` has all required variables:

```bash
# Check MSSQL settings
grep MSSQL .env

# Check PostgreSQL settings  
grep POSTGRES .env
```

Required variables:
- ✅ MSSQL_HOST
- ✅ MSSQL_USER
- ✅ MSSQL_PASS
- ✅ MSSQL_DB_HRM
- ✅ POSTGRES_HOST
- ✅ POSTGRES_USER
- ✅ POSTGRES_PASSWORD
- ✅ POSTGRES_DB

---

## 🚀 Common Tasks

### Sync for a Different Year
```bash
python app/cli_sync.py --sync-kpi --year 2024
```

### Sync Multiple Years
```bash
for year in 2023 2024 2025; do
  python app/cli_sync.py --sync-kpi --year $year
done
```

### Check Sync Status
```bash
python app/cli_sync.py --status
```

### View Logs
```bash
tail -f /app/logs/sync_service.log
```

### Check Data in PostgreSQL
```bash
psql -h postgres-db -U admincomp -d kpidb
SELECT COUNT(*) FROM public.data;
SELECT DISTINCT year FROM public.data;
SELECT * FROM public.data LIMIT 10;
```

---

## 📚 Documentation Guide

Pick your path based on what you need:

### 👤 I'm a User (Want to Use It)
→ Read: [MONTHLY_KPI_QUICK_START.md](MONTHLY_KPI_QUICK_START.md)
- Quick commands
- 3 ways to use it
- Basic troubleshooting

### 👨‍💻 I'm a Developer (Want to Understand It)
→ Read: [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md)
- Technical implementation
- Database schema
- Error handling
- Full API reference

### 📊 I'm a Manager (Want an Overview)
→ Read: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- What was done
- How it works
- Key features
- Next steps

### 🏗️ I'm Setting It Up
→ Read: [README_SYNC_FEATURE.md](README_SYNC_FEATURE.md)
- Complete setup guide
- Configuration details
- Troubleshooting
- Learning resources

### 🧪 I Want to Learn by Example
→ Run: `python example_usage.py`
- Interactive examples
- Real-world use cases
- Error handling demo

---

## 🔍 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "Connection failed" | Run `python app/cli_sync.py --validate` |
| "No data returned" | Check if data exists in MSSQL for that year |
| "Table not found" | Create table in PostgreSQL or check schema |
| "Permission denied" | Verify credentials in `.env` |
| "Stored procedure not found" | Check procedure exists in MSSQL |

**For detailed help:** See [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md#troubleshooting)

---

## 🎓 Learning Path

### Day 1: Get It Working
1. ✅ Read this checklist (5 min)
2. ✅ Run validation (2 min)
3. ✅ Run first sync (5 min)
4. ✅ Verify data (5 min)
**Total: 17 minutes**

### Day 2: Understand It
1. Read [MONTHLY_KPI_QUICK_START.md](MONTHLY_KPI_QUICK_START.md) (10 min)
2. Try different years (10 min)
3. Read [README_SYNC_FEATURE.md](README_SYNC_FEATURE.md) (20 min)
**Total: 40 minutes**

### Day 3: Master It
1. Read [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md) (30 min)
2. Run `example_usage.py` (15 min)
3. Review code in `sync_service.py` (20 min)
**Total: 65 minutes**

---

## 🎯 Success Criteria

You'll know it's working when:

- [ ] `python cli_sync.py --validate` shows all connections OK
- [ ] `python cli_sync.py --sync-kpi --year 2025` completes successfully
- [ ] PostgreSQL query returns rows: `SELECT COUNT(*) FROM public.data;`
- [ ] API endpoint returns status "success"
- [ ] Logs show: "✓ Successfully saved [N] rows to public.data"

---

## 💡 Pro Tips

1. **Schedule Regular Syncs**
   ```bash
   # Linux: Add to crontab
   0 2 * * * cd /path/to/app && python cli_sync.py --sync-kpi --year $(date +\%Y)
   ```

2. **Monitor with Logs**
   ```bash
   # Keep logs window open
   tail -f /app/logs/sync_service.log
   ```

3. **Batch Process Multiple Years**
   ```bash
   # Sync last 3 years
   for y in 2023 2024 2025; do
     echo "Syncing $y..."
     python cli_sync.py --sync-kpi --year $y
   done
   ```

4. **Check Before Syncing**
   ```bash
   # Validate everything first
   python cli_sync.py --validate && python cli_sync.py --status
   ```

---

## 📞 Need Help?

1. **Quick Issue?** → Check [Troubleshooting](#-troubleshooting-quick-reference) above
2. **Technical Question?** → See [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md)
3. **How to Use?** → See [MONTHLY_KPI_QUICK_START.md](MONTHLY_KPI_QUICK_START.md)
4. **Setup Help?** → See [README_SYNC_FEATURE.md](README_SYNC_FEATURE.md)

---

## ✅ You're All Set!

Everything is ready to use. Start with:

```bash
python app/cli_sync.py --sync-kpi --year 2025
```

Good luck! 🚀

---

**Quick Reference:**
- 📖 Main docs: [README_SYNC_FEATURE.md](README_SYNC_FEATURE.md)
- ⚡ Quick start: [MONTHLY_KPI_QUICK_START.md](MONTHLY_KPI_QUICK_START.md)  
- 🔧 Technical: [MONTHLY_KPI_SYNC.md](MONTHLY_KPI_SYNC.md)
- 📊 Summary: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- 🧪 Examples: `python example_usage.py`

**Last Updated:** April 23, 2025
