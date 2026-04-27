"""
KPI Pro - Data Synchronization System
Main Flask application entry point
"""

from flask import Flask, request
from routes.data_routes import data_bp
import os
import logging
from pathlib import Path

# Create Flask app
app = Flask(__name__)

# ==================== Configuration ====================

# Create logs directory if it doesn't exist
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)

# Configure Flask logging
if not app.debug:
    try:
        # Production logging
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    except PermissionError:
        # Fallback to console logging if file logging fails
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

app.logger.setLevel(logging.INFO)
app.logger.info("KPI Pro application initialized")

# Configure application settings
app.config.update(
    JSON_SORT_KEYS=False,
    JSONIFY_PRETTYPRINT_REGULAR=True,
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max request size
)

# ==================== Register Blueprints ====================

app.register_blueprint(data_bp)

# ==================== Global Error Handlers ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    app.logger.warning(f"404 error: {error}")
    return {"status": "error", "message": "Resource not found"}, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    app.logger.error(f"500 error: {error}", exc_info=True)
    return {"status": "error", "message": "Internal server error"}, 500


@app.before_request
def before_request():
    """Log incoming requests"""
    app.logger.debug(f"{request.method} {request.path}")


# ==================== Application Entry Point ====================

if __name__ == "__main__":
    import sys
    
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.logger.info(f"Starting KPI Pro on {host}:{port} (debug={debug_mode})")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            use_reloader=debug_mode
        )
    except Exception as e:
        app.logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        sys.exit(1)