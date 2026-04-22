# 🚀 Quick Start Guide - KPI Pro

## ✨ What Was Done

All critical issues have been resolved:

| Component | Status | Details |
|-----------|--------|---------|
| **Dockerfile** | ✅ Complete | Production-ready with health checks |
| **HTML Templates** | ✅ Complete | Responsive pages for sync & dashboard |
| **CSS Styling** | ✅ Complete | Modern design, fully responsive |
| **JavaScript** | ✅ Complete | Interactive UI with error handling |
| **Backend Services** | ✅ Enhanced | Comprehensive logging and error handling |
| **API Endpoints** | ✅ Enhanced | Status and health check endpoints added |

---

## 🏃 Quick Start (5 Minutes)

### 1. Configure Environment
```bash
cd /home/admincomp/workspace/kpi-pro

# Copy example config
cp .env.example .env

# Edit with your database credentials
nano .env
```

### 2. Build and Run
```bash
# Start containers
docker-compose up --build

# Application is ready at:
# 🌐 http://localhost:5020
```

### 3. Test the System
```bash
# Check health
curl http://localhost:5020/api/health

# Get status
curl http://localhost:5020/api/status

# Trigger sync (POST request)
curl -X POST http://localhost:5020/sync
```

---

## 📁 Key Files Created/Updated

### New Files
- ✅ `app/Dockerfile` - Docker configuration
- ✅ `app/templates/base.html` - Master template
- ✅ `app/templates/index.html` - Sync page
- ✅ `app/templates/dashboard.html` - Dashboard
- ✅ `app/static/css/style.css` - Styling
- ✅ `app/static/js/script.js` - Interactivity
- ✅ `.env.example` - Configuration template
- ✅ `DEVELOPMENT.md` - Full documentation

### Updated Files
- ✅ `app/main.py` - Better logging and configuration
- ✅ `app/services/sync_service.py` - Error handling and logging
- ✅ `app/routes/data_routes.py` - Enhanced endpoints

---

## 🎯 Features Overview

### 🔄 Data Synchronization
- Click "Start Sync" button to begin
- Real-time status updates
- Row count confirmation
- Error messages if anything fails

### 📊 Dashboard
- View KPI statistics
- Search and filter data
- Pagination support
- Activity log

### ⌨️ Keyboard Shortcuts
- **Ctrl+S** - Trigger sync
- **Ctrl+R** - Reset status

### 📝 Activity Logging
- All operations logged to `/app/logs/`
- `app.log` - Application logs
- `sync_service.log` - Sync operation logs

---

## 🔍 Monitor the Application

### View Logs in Real-time
```bash
# Docker container logs
docker-compose logs -f kpi-sync-app

# Or inside container
docker exec kpi_sync_service tail -f /app/logs/sync_service.log
```

### Check Status
```bash
# API Status Endpoint
curl http://localhost:5020/api/status | jq

# Health Check
curl http://localhost:5020/api/health | jq
```

---

## 🐛 Troubleshooting

### Issue: Container fails to start
```bash
# Check logs
docker-compose logs kpi-sync-app

# Make sure .env is configured
cat .env | grep MSSQL
```

### Issue: Database connection errors
1. Verify SQL Server is accessible from Docker network
2. Verify PostgreSQL is running and accessible
3. Check `.env` credentials match your databases
4. Use `/api/status` endpoint to test connections

### Issue: Sync returns 0 rows
- Check if `Source_Table` exists in SQL Server
- Verify user permissions on the source table
- Check logs: `docker exec kpi_sync_service tail -f /app/logs/sync_service.log`

---

## 📞 API Reference

### POST /sync
```bash
curl -X POST http://localhost:5020/sync
```
Response:
```json
{
  "status": "success",
  "rows": 8449,
  "message": "Successfully synced 8449 rows"
}
```

### GET /api/status
```bash
curl http://localhost:5020/api/status
```

### GET /api/health
```bash
curl http://localhost:5020/api/health
```

---

## 📚 Documentation

For detailed information, see:
- **`DEVELOPMENT.md`** - Full development guide
- **`readme.md`** - Project overview
- **`docker-compose.yml`** - Container configuration

---

## ✅ What's Next?

1. **Configure** `.env` with your database credentials
2. **Start** with `docker-compose up --build`
3. **Visit** http://localhost:5020
4. **Click** "Start Sync" button
5. **Monitor** the logs and activity

---

**Happy syncing! 🎉**

Need help? Check the logs or refer to DEVELOPMENT.md for detailed troubleshooting.
