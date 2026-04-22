"""
Data Routes
API endpoints for KPI data synchronization and retrieval
"""

from flask import Blueprint, render_template, request, jsonify, current_app
import logging
from services.sync_service import sync_kpi_data, validate_connection, get_sync_status

# Create logger
logger = logging.getLogger(__name__)

data_bp = Blueprint('data', __name__)


@data_bp.route('/')
def index():
    """
    Render the main index page
    """
    return render_template('index.html')


@data_bp.route('/dashboard')
def dashboard():
    """
    Render the dashboard page
    """
    return render_template('dashboard.html')

@data_bp.route('/report')
def report():
    """
    Render the report page
    """
    return render_template('report.html')


@data_bp.route('/api/report', methods=['GET'])
def get_report_data():
    """
    Get pivoted KPI data for the report
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text
    
    year = request.args.get('year', 2025, type=int)
    
    query = text(f"""
        SELECT 
            kpi_id, 
            MAX(CASE WHEN month = 1 THEN value END) AS m1,
            MAX(CASE WHEN month = 2 THEN value END) AS m2,
            MAX(CASE WHEN month = 3 THEN value END) AS m3,
            MAX(CASE WHEN month = 4 THEN value END) AS m4,
            MAX(CASE WHEN month = 5 THEN value END) AS m5,
            MAX(CASE WHEN month = 6 THEN value END) AS m6,
            MAX(CASE WHEN month = 7 THEN value END) AS m7,
            MAX(CASE WHEN month = 8 THEN value END) AS m8,
            MAX(CASE WHEN month = 9 THEN value END) AS m9,
            MAX(CASE WHEN month = 10 THEN value END) AS m10,
            MAX(CASE WHEN month = 11 THEN value END) AS m11,
            MAX(CASE WHEN month = 12 THEN value END) AS m12
        FROM public.data
        WHERE year = {year}
        GROUP BY kpi_id
        ORDER BY kpi_id
    """)
    
    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            result = conn.execute(query)
            # Convert result to list of dicts
            data = [dict(row._mapping) for row in result]
            
            return jsonify({
                "status": "success",
                "year": year,
                "data": data
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@data_bp.route('/sync', methods=['POST'])
def run_sync():
    """
    Trigger KPI data synchronization
    POST /sync
    
    Returns:
        JSON response with status and result
    """
    logger.info("Received sync request")
    
    try:
        # Call sync service
        rows_synced, error = sync_kpi_data()
        
        if error is None:
            # Success
            logger.info(f"Sync successful: {rows_synced} rows")
            return jsonify({
                "status": "success",
                "rows": rows_synced,
                "message": f"Successfully synced {rows_synced} rows"
            }), 200
        else:
            # Error during sync
            logger.error(f"Sync failed: {error}")
            return jsonify({
                "status": "error",
                "rows": 0,
                "error": error
            }), 400
    
    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error during sync: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({
            "status": "error",
            "error": error_msg
        }), 500


@data_bp.route('/api/status', methods=['GET'])
def status():
    """
    Get current system status
    GET /api/status
    
    Returns:
        JSON response with system status
    """
    try:
        is_valid, msg = validate_connection()
        sync_status = get_sync_status()
        
        return jsonify({
            "connections": {
                "valid": is_valid,
                "message": msg
            },
            "sync": sync_status
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@data_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    GET /api/health
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        "status": "healthy",
        "service": "KPI Sync Service",
        "version": "1.0.0"
    }), 200


@data_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({
        "status": "error",
        "error": "Endpoint not found"
    }), 404


@data_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({
        "status": "error",
        "error": "Internal server error"
    }), 500