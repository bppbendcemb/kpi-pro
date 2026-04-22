# KPI Pro - Development Guide

## Project Overview

KPI Pro is a **Key Performance Indicator Data Synchronization System** that automatically syncs performance metrics from SQL Server to PostgreSQL with a modern web interface.

## Recent Improvements (This Session)

### ✅ 1. Docker Configuration
- **File**: `app/Dockerfile`
- **Created**: Fully functional Dockerfile with:
  - Python 3.11-slim base image
  - System dependencies for SQL Server and PostgreSQL drivers
  - Automatic dependency installation
  - Health checks
  - Production-ready configuration

### ✅ 2. Frontend Templates
Created responsive HTML templates with Jinja2 templating:

- **base.html**: Master template with navigation, footer, and styling
- **index.html**: Main sync page with:
  - Data synchronization controls
  - Status monitoring
  - System information cards
  - Feature showcase
- **dashboard.html**: KPI dashboard with:
  - Statistics cards
  - Chart placeholders (ready for Chart.js integration)
  - Data table with pagination
  - Search and filter capabilities
  - Activity log

### ✅ 3. Styling & UI
- **File**: `app/static/css/style.css`
- **Features**:
  - Modern gradient design with professional color scheme
  - Fully responsive (mobile, tablet, desktop)
  - Accessibility features
  - Smooth animations and transitions
  - Dark mode ready
  - Print-friendly styles

### ✅ 4. Interactive JavaScript
- **File**: `app/static/js/script.js`
- **Features**:
  - Async data synchronization with real-time status
  - Activity logging system
  - Search and filter functionality
  - Pagination support
  - Keyboard shortcuts (Ctrl+S to sync)
  - Error handling with user-friendly messages
  - CSV export functionality
  - Global error handlers

### ✅ 5. Enhanced Backend Services

#### Sync Service (`app/services/sync_service.py`)
Comprehensive improvements:
- **Structured logging**: All operations logged to file and console
- **Error handling**: Detailed error messages and recovery
- **Data validation**: Duplicate detection, null value checking
- **Progress tracking**: Step-by-step execution logging
- **Connection management**: Proper resource cleanup
- **Helper functions**:
  - `sync_kpi_data()`: Main sync function with error reporting
  - `validate_connection()`: Database connection validation
  - `get_sync_status()`: System status monitoring

#### Routes (`app/routes/data_routes.py`)
Enhanced API with new endpoints:
- `GET /` - Main index page
- `GET /dashboard` - Dashboard page
- `POST /sync` - Trigger synchronization
- `GET /api/status` - Get system status
- `GET /api/health` - Health check endpoint
- Proper error handlers for 404 and 500 errors

#### Main Application (`app/main.py`)
Production-ready configuration:
- Automatic logs directory creation
- Comprehensive logging setup
- Configuration management via environment variables
- Global error handlers
- Request logging
- Graceful error handling

## Directory Structure

```
app/
├── Dockerfile                 ✅ New: Complete Docker configuration
├── main.py                   ✅ Enhanced: Better error handling and logging
├── requirements.txt          ✓ Python dependencies
├── config/
│   ├── db_config.py         ✓ Database connections
│   ├── mssql_config.py      (unused - can be removed)
│   └── pg_config.py         (unused - can be removed)
├── models/
│   └── kpi_model.py         (empty - ready for SQLAlchemy models)
├── routes/
│   └── data_routes.py       ✅ Enhanced: Better error handling
├── services/
│   └── sync_service.py      ✅ Enhanced: Logging and error handling
├── templates/
│   ├── base.html            ✅ New: Master template
│   ├── index.html           ✅ New: Main sync page
│   └── dashboard.html       ✅ New: Data dashboard
├── static/
│   ├── css/
│   │   └── style.css        ✅ New: Complete styling
│   └── js/
│       └── script.js        ✅ New: Interactive functionality
└── logs/                     ✓ Created automatically at runtime
```

## Environment Configuration

### Setup .env File
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### Required Environment Variables
```
# PostgreSQL (Destination)
PG_HOST=postgres-db
PG_PORT=5432
PG_USER=your_postgres_user
PG_PASS=your_postgres_password
PG_DB=your_database_name

# SQL Server (Source)
MSSQL_HOST=192.168.x.x
MSSQL_PORT=1433
MSSQL_USER=sa
MSSQL_PASS=your_mssql_password
MSSQL_DB=your_source_db

# Flask (Optional)
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=False
```

## Running the Application

### Using Docker Compose
```bash
cd /home/admincomp/workspace/kpi-pro

# Build and start containers
docker-compose up --build

# Access the application
# Home: http://localhost:5020
# Sync Page: http://localhost:5020/
# Dashboard: http://localhost:5020/dashboard
# API Status: http://localhost:5020/api/status
# Health Check: http://localhost:5020/api/health
```

### Local Development
```bash
cd /home/admincomp/workspace/kpi-pro/app

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000
export DEBUG=True

# Run Flask
python main.py
```

## Features & Usage

### 1. Data Synchronization
- **Endpoint**: POST `/sync`
- **How it works**:
  1. Connects to SQL Server and reads from `Source_Table`
  2. Validates data (removes duplicates, checks for nulls)
  3. Connects to PostgreSQL and writes to `kpi_data` table
  4. Returns row count and error messages (if any)

### 2. Real-time Status Monitoring
- **Endpoint**: GET `/api/status`
- Returns current sync status and connection health

### 3. Health Checks
- **Endpoint**: GET `/api/health`
- For monitoring and container health checks

### 4. Interactive UI
- Start sync with button or Ctrl+S keyboard shortcut
- Real-time status updates
- Activity log with timestamps
- Search and filter data
- Pagination support

## Logging

### Log Files
- **Application Log**: `/app/logs/app.log`
- **Sync Service Log**: `/app/logs/sync_service.log`

### Log Format
```
2026-04-22 14:30:45,123 - sync_service - INFO - Starting KPI data synchronization
2026-04-22 14:30:45,456 - sync_service - INFO - Step 1: Connecting to SQL Server...
```

### Log Levels
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages
- `WARNING`: Warning messages for unexpected situations
- `ERROR`: Error messages for failures
- `CRITICAL`: Critical errors that may halt execution

## Troubleshooting

### Docker Container Won't Start
```bash
# Check logs
docker-compose logs kpi-sync-app

# Verify connections
docker exec kpi_sync_service python -c "from services.sync_service import validate_connection; print(validate_connection())"
```

### Database Connection Errors
1. Verify `.env` file has correct credentials
2. Check if databases are running and accessible
3. Test connection: `curl http://localhost:5020/api/status`

### Logs Not Appearing
- Ensure `/app/logs` directory exists (created automatically)
- Check file permissions
- Verify logging configuration in `sync_service.py` and `main.py`

## Next Steps / Future Enhancements

### High Priority
- [ ] Replace chart placeholders with Chart.js/Plotly
- [ ] Add more detailed data views and analysis
- [ ] Implement incremental sync (vs full replace)
- [ ] Add user authentication and authorization
- [ ] Create admin dashboard for configuration

### Medium Priority
- [ ] Add scheduling capability (e.g., cron jobs)
- [ ] Email notifications on sync failures
- [ ] Data transformation/mapping rules
- [ ] SQLAlchemy ORM models for type safety
- [ ] Database migration system (Alembic)

### Low Priority
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Data export functionality
- [ ] Sync history/analytics
- [ ] API rate limiting

## API Documentation

### POST /sync
Trigger data synchronization

**Request**: `POST /sync`

**Response** (Success):
```json
{
    "status": "success",
    "rows": 8449,
    "message": "Successfully synced 8449 rows"
}
```

**Response** (Error):
```json
{
    "status": "error",
    "rows": 0,
    "error": "Failed to connect to SQL Server: ..."
}
```

### GET /api/status
Get system status

**Request**: `GET /api/status`

**Response**:
```json
{
    "connections": {
        "valid": true,
        "message": "All connections validated successfully"
    },
    "sync": {
        "status": "healthy",
        "destination_table": "kpi_data",
        "row_count": 8449
    }
}
```

### GET /api/health
Health check

**Request**: `GET /api/health`

**Response**:
```json
{
    "status": "healthy",
    "service": "KPI Sync Service",
    "version": "1.0.0"
}
```

## Code Quality

- ✅ All Python files validated for syntax errors
- ✅ Comprehensive error handling throughout
- ✅ Type hints in critical functions
- ✅ Detailed docstrings and comments
- ✅ Follows PEP 8 style guidelines
- ✅ Responsive and accessible HTML/CSS

## Contact & Support

For issues or questions about this enhanced version, refer to the original project documentation or check the logs in `/app/logs/`.

---

**Last Updated**: April 22, 2026
**Version**: 1.0.0 (Enhanced)
