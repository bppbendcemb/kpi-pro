"""
Data Routes
API endpoints for KPI data synchronization and retrieval
"""

from flask import Blueprint, render_template, request, jsonify, current_app
import logging
from datetime import datetime
from services.sync_service import (
    sync_kpi_data,
    validate_connection,
    get_sync_status,
    sync_monthly_kpi_report,
)

# Create logger
logger = logging.getLogger(__name__)

data_bp = Blueprint("data", __name__)


@data_bp.route("/")
def index():
    """
    Render the main index page
    """
    return render_template("index.html")


@data_bp.route("/dashboard")
def dashboard():
    """
    Render the dashboard page
    """
    return render_template("dashboard.html")


@data_bp.route("/report")
def show_report():
    """
    Render the report page
    """
    current_year = datetime.now().year
    return render_template("report.html", current_year=current_year)


@data_bp.route("/api/report", methods=["GET"])
def get_report_data():
    """
    Get pivoted KPI data for the report
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    current_year = datetime.now().year
    year = request.args.get("year", current_year, type=int)

    query = text(
        f"""
          SELECT 
    dt.kpi_id, 
    MAX(CASE WHEN dt.month = 1 THEN dt.value END) AS m1,
    MAX(CASE WHEN dt.month = 2 THEN dt.value END) AS m2,
    MAX(CASE WHEN dt.month = 3 THEN dt.value END) AS m3,
    MAX(CASE WHEN dt.month = 4 THEN dt.value END) AS m4,
    MAX(CASE WHEN dt.month = 5 THEN dt.value END) AS m5,
    MAX(CASE WHEN dt.month = 6 THEN dt.value END) AS m6,
    MAX(CASE WHEN dt.month = 7 THEN dt.value END) AS m7,
    MAX(CASE WHEN dt.month = 8 THEN dt.value END) AS m8,
    MAX(CASE WHEN dt.month = 9 THEN dt.value END) AS m9,
    MAX(CASE WHEN dt.month = 10 THEN dt.value END) AS m10,
    MAX(CASE WHEN dt.month = 11 THEN dt.value END) AS m11,
    MAX(CASE WHEN dt.month = 12 THEN dt.value END) AS m12,
    act.group_id, 
    act.department_id, 
    act."no", 
    act.sub_no, 
    act.activities, 
    act.description, 
    act.description2, 
    act."source", 
    act."linkUrl", 
    act.unit, 
    act.istarget,
	dp.department_id, 
	dp.department_desc,
	grp.group_id, 
    grp.group_desc,
    gl.target AS year_target
FROM public.data AS dt
LEFT JOIN public.activities AS act ON dt.kpi_id = act.kpi_id
LEFT JOIN public.department AS dp ON act.department_id = dp.department_id
LEFT JOIN public."group" AS grp ON act.group_id = grp.group_id
LEFT JOIN public.goals AS gl ON dt.kpi_id = gl.kpi_id AND gl.year = dt.year
WHERE dt.year = {year}
GROUP BY 
    dt.kpi_id, 
    act.group_id, 
    act.department_id, 
    act."no", 
    act.sub_no, 
    act.activities, 
    act.description, 
    act.description2, 
    act."source", 
    act."linkUrl", 
    act.unit, 
    act.istarget,
	dp.department_id, 
	dp.department_desc,
	grp.group_id, 
    grp.group_desc,
    gl.target
ORDER BY CAST(dt.kpi_id AS INTEGER);

    """
    )

    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            result = conn.execute(query)
            # Convert result to list of dicts
            data = [dict(row._mapping) for row in result]

            return jsonify({"status": "success", "year": year, "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@data_bp.route("/sync", methods=["POST"])
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
            return (
                jsonify(
                    {
                        "status": "success",
                        "rows": rows_synced,
                        "message": f"Successfully synced {rows_synced} rows",
                    }
                ),
                200,
            )
        else:
            # Error during sync
            logger.error(f"Sync failed: {error}")
            return jsonify({"status": "error", "rows": 0, "error": error}), 400

    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error during sync: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({"status": "error", "error": error_msg}), 500

@data_bp.route("/api/sync/monthly-kpi", methods=["POST"])
def sync_monthly_kpi():
    """
    Execute MSSQL stored procedure and sync monthly KPI report to PostgreSQL
    EXEC [dbo].[sp_GetMonthlyKPIReport] @yr = 2025;
    ดึงข้อมูล KPI รายเดือนจาก MSSQL มาบันทึกลง PostgreSQL

    POST /api/sync/monthly-kpi
    JSON Body:
        {
            "year": 2025
        }

    Returns:
        JSON response with status and result
    """
    logger.info("Received monthly KPI report sync request")

    try:
        # Get year from request body, default to current year
        data = request.get_json() or {}
        current_year = datetime.now().year
        year = data.get("year", current_year)

        logger.info(f"Syncing monthly KPI report for year: {year}")

        # Call sync service
        rows_synced, error = sync_monthly_kpi_report(year=year)

        if error is None:
            # Success
            logger.info(f"Monthly KPI sync successful: {rows_synced} rows")
            return (
                jsonify(
                    {
                        "status": "success",
                        "year": year,
                        "rows": rows_synced,
                        "message": f"Successfully synced {rows_synced} rows from sp_GetMonthlyKPIReport",
                    }
                ),
                200,
            )
        else:
            # Error during sync
            logger.error(f"Monthly KPI sync failed: {error}")
            return (
                jsonify({"status": "error", "year": year, "rows": 0, "error": error}),
                400,
            )

    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error during monthly KPI sync: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({"status": "error", "error": error_msg}), 500


@data_bp.route("/api/status", methods=["GET"])
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

        return (
            jsonify(
                {
                    "connections": {"valid": is_valid, "message": msg},
                    "sync": sync_status,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error getting status: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "error": str(e)}), 500


@data_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    GET /api/health

    Returns:
        JSON response with health status
    """
    return (
        jsonify(
            {"status": "healthy", "service": "KPI Sync Service", "version": "1.0.0"}
        ),
        200,
    )

@data_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({"status": "error", "error": "Endpoint not found"}), 404

@data_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({"status": "error", "error": "Internal server error"}), 500

@data_bp.route("/api/data/get-monthly", methods=["GET"])
def get_monthly_data():
    """
    Get monthly KPI data for a specific year and month
    GET /api/data/get-monthly?year=2024&month=1

    Returns:
        JSON response with monthly data
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if not year or not month:
        return jsonify({"success": False, "error": "Year and month are required"}), 400

    query = text(
        f"""
        SELECT 
            dt.kpi_id,
            dt.value,
            dt.year,
            dt.month
        FROM public.data AS dt
        WHERE dt.year = {year} AND dt.month = {month}
        ORDER BY dt.kpi_id
    """
    )

    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            result = conn.execute(query)
            data = [dict(row._mapping) for row in result]

            return jsonify({"success": True, "data": data}), 200

    except Exception as e:
        logger.error(f"Error fetching monthly data: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

@data_bp.route("/api/data/batch-add", methods=["POST"])
def batch_add_data():
    """
    Add/Update multiple KPI data entries
    POST /api/data/batch-add
    JSON: { "year": 2026, "month": 1, "data": [{ "kpi_id": 1, "value": 100 }, ...] }
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"success": False, "error": "No data provided"}), 400

        year = payload.get("year")
        month = payload.get("month")
        kpi_list = payload.get("data", [])

        if not year or not month or not kpi_list:
            return (
                jsonify({"success": False, "error": "Missing year, month or data"}),
                400,
            )

        engine = get_pg_engine()
        with engine.connect() as conn:
            # Prepare batch upsert
            query = text(
                """
                INSERT INTO public.data (kpi_id, year, month, value)
                VALUES (:kpi_id, :year, :month, :value)
                ON CONFLICT (kpi_id, year, month) 
                DO UPDATE SET value = EXCLUDED.value
            """
            )

            # Execute in transaction
            for item in kpi_list:
                conn.execute(
                    query,
                    {
                        "kpi_id": item["kpi_id"],
                        "year": year,
                        "month": month,
                        "value": item["value"],
                    },
                )
            conn.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "count": len(kpi_list),
                    "message": f"Successfully upserted {len(kpi_list)} records",
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error in batch add: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

@data_bp.route("/api/kpi/<int:kpi_id>/link", methods=["GET"])
def get_kpi_link(kpi_id):
    """
    Get linkUrl for a specific KPI ID
    GET /api/kpi/<kpi_id>/link

    Returns:
        JSON response with linkUrl
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    try:
        query = text(
            """
            SELECT kpi_id, "linkUrl" 
            FROM public.activities 
            WHERE kpi_id = :kpi_id
            LIMIT 1
        """
        )

        engine = get_pg_engine()
        with engine.connect() as conn:
            result = conn.execute(query, {"kpi_id": kpi_id})
            row = result.fetchone()

            if row:
                data = dict(row._mapping)
                return (
                    jsonify(
                        {
                            "status": "success",
                            "kpi_id": data["kpi_id"],
                            "linkUrl": data.get("linkUrl"),
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify({"status": "error", "message": "KPI ID not found"}),
                    404,
                )

    except Exception as e:
        logger.error(f"Error fetching KPI link: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "error": str(e)}), 500

@data_bp.route("/api/query2", methods=["GET"])
def get_query2_data():
    """
    Get data from query2 - existing KPI data for current year with monthly values
    GET /api/query2

    Returns:
        JSON response with query2 data
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    current_year = request.args.get("year", datetime.now().year, type=int)

    query2 = text(
        f"""
         SELECT
    dt.kpi_id,
    MAX(CASE WHEN dt.month = 1 THEN dt.value END) AS m1,
    MAX(CASE WHEN dt.month = 2 THEN dt.value END) AS m2,
    MAX(CASE WHEN dt.month = 3 THEN dt.value END) AS m3,
    MAX(CASE WHEN dt.month = 4 THEN dt.value END) AS m4,
    MAX(CASE WHEN dt.month = 5 THEN dt.value END) AS m5,
    MAX(CASE WHEN dt.month = 6 THEN dt.value END) AS m6,
    MAX(CASE WHEN dt.month = 7 THEN dt.value END) AS m7,
    MAX(CASE WHEN dt.month = 8 THEN dt.value END) AS m8,
    MAX(CASE WHEN dt.month = 9 THEN dt.value END) AS m9,
    MAX(CASE WHEN dt.month = 10 THEN dt.value END) AS m10,
    MAX(CASE WHEN dt.month = 11 THEN dt.value END) AS m11,
    MAX(CASE WHEN dt.month = 12 THEN dt.value END) AS m12,
    act.group_id,
    act.department_id,
    act."no",
    act.sub_no,
    act.activities,
    act.description,
    act.description2,
    act."source",
    act."linkUrl",
    act.unit,
    act.source_result,
    act.istarget,
	dp.department_id,
	dp.department_desc,
	grp.group_id,
    grp.group_desc
FROM public.data AS dt
LEFT JOIN public.activities AS act ON dt.kpi_id = act.kpi_id
LEFT JOIN public.department AS dp ON act.department_id = dp.department_id
LEFT JOIN public."group" AS grp ON act.group_id = grp.group_id
WHERE dt.year = {current_year}
GROUP BY
    dt.kpi_id,
    act.group_id,
    act.department_id,
    act."no",
    act.sub_no,
    act.activities,
    act.description,
    act.description2,
    act."source",
    act."linkUrl",
    act.unit,
    act.source_result,
    act.istarget,
	dp.department_id,
	dp.department_desc,
	grp.group_id,
    grp.group_desc
ORDER BY CAST(dt.kpi_id AS INTEGER);
    """
    )

    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            result = conn.execute(query2)
            data = [dict(row._mapping) for row in result]

            return (
                jsonify(
                    {
                        "status": "success",
                        "year": current_year,
                        "count": len(data),
                        "data": data,
                        "message": f"Successfully retrieved {len(data)} KPI records with monthly data for {current_year}",
                    }
                ),
                200,
            )

    except Exception as e:
        logger.error(f"Error fetching query2 data: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "error": str(e)}), 500

@data_bp.route("/add", methods=["GET", "POST"])
def add_data():
    """
    Add new KPI data entry
    GET /add - Show form
    POST /add - Handle form submission
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    if request.method == "POST":
        try:
            # Handle both JSON and Form data
            if request.is_json:
                data = request.get_json()
                kpi_id = data.get("kpi_id")
                year = data.get("year")
                month = data.get("month")
                value = data.get("value")
            else:
                kpi_id = request.form.get("kpi_id")
                year = request.form.get("year")
                month = request.form.get("month")
                value = request.form.get("value")

            if not all([kpi_id, year, month, value]):
                return (
                    jsonify({"success": False, "error": "All fields are required"}),
                    400,
                )

            engine = get_pg_engine()
            with engine.connect() as conn:
                conn.execute(
                    text(
                        """
                    INSERT INTO public.data (kpi_id, year, month, value)
                    VALUES (:kpi_id, :year, :month, :value)
                    ON CONFLICT (kpi_id, year, month) 
                    DO UPDATE SET value = EXCLUDED.value
                """
                    ),
                    {"kpi_id": kpi_id, "year": year, "month": month, "value": value},
                )
                conn.commit()

            return (
                jsonify({"success": True, "message": "KPI added/updated successfully"}),
                200,
            )

        except Exception as e:
            logger.error(f"Error adding KPI: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    current_year = datetime.now().year
    kpi_ids = list(range(1, 89))

    query = text(
        f"""
SELECT 
ac.kpi_id, 
ac.group_id, 
ac.department_id, 
ac.no, 
ac.sub_no, 
ac.activities, 
ac.description, 
ac.description2, 
ac.source, 
ac."linkUrl", 
ac.unit, 
ac.source_result, 
ac.istarget,
ac.active, 
dp.department_desc
FROM public.activities AS ac
LEFT JOIN public.department AS dp ON ac.department_id = dp.department_id

    """
    )

    query2 = text(
        f"""
         SELECT 
    dt.kpi_id, 
    MAX(CASE WHEN dt.month = 1 THEN dt.value END) AS m1,
    MAX(CASE WHEN dt.month = 2 THEN dt.value END) AS m2,
    MAX(CASE WHEN dt.month = 3 THEN dt.value END) AS m3,
    MAX(CASE WHEN dt.month = 4 THEN dt.value END) AS m4,
    MAX(CASE WHEN dt.month = 5 THEN dt.value END) AS m5,
    MAX(CASE WHEN dt.month = 6 THEN dt.value END) AS m6,
    MAX(CASE WHEN dt.month = 7 THEN dt.value END) AS m7,
    MAX(CASE WHEN dt.month = 8 THEN dt.value END) AS m8,
    MAX(CASE WHEN dt.month = 9 THEN dt.value END) AS m9,
    MAX(CASE WHEN dt.month = 10 THEN dt.value END) AS m10,
    MAX(CASE WHEN dt.month = 11 THEN dt.value END) AS m11,
    MAX(CASE WHEN dt.month = 12 THEN dt.value END) AS m12,
    act.group_id, 
    act.department_id, 
    act."no", 
    act.sub_no, 
    act.activities, 
    act.description, 
    act.description2, 
    act."source", 
    act."linkUrl", 
    act.unit, 
    act.source_result, 
    act.istarget,
	dp.department_id, 
	dp.department_desc,
	grp.group_id, 
    grp.group_desc
FROM public.data AS dt
LEFT JOIN public.activities AS act ON dt.kpi_id = act.kpi_id
LEFT JOIN public.department AS dp ON act.department_id = dp.department_id
LEFT JOIN public."group" AS grp ON act.group_id = grp.group_id
WHERE dt.year = {current_year}
GROUP BY 
    dt.kpi_id, 
    act.group_id, 
    act.department_id, 
    act."no", 
    act.sub_no, 
    act.activities, 
    act.description, 
    act.description2, 
    act."source", 
    act."linkUrl", 
    act.unit, 
    act.source_result, 
    act.istarget,
	dp.department_id, 
	dp.department_desc,
	grp.group_id, 
    grp.group_desc
ORDER BY CAST(dt.kpi_id AS INTEGER);

      
    """
    )

    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            # 1. ดึงรายชื่อ KPI ทั้งหมด (สำหรับ Dropdown หรือรายการหลัก)
            result_all = conn.execute(query)
            kpi_list = [dict(row._mapping) for row in result_all]
            
            # Use the pre-defined query2 which already includes the current_year
            query2_dynamic = query2
            result_existing = conn.execute(query2_dynamic)
            existing_data = [dict(row._mapping) for row in result_existing]

            return render_template(
                "add.html", 
                year=current_year, 
                kpi_ids=kpi_ids, 
                kpi_data=kpi_list,         # รายชื่อ KPI ทั้งหมด
                existing_data=existing_data # ข้อมูลรายเดือนที่กรอกแล้ว
            )
    except Exception as e:
        logger.error(f"Error fetching KPI data: {str(e)}", exc_info=True)

    return render_template("add.html", year=current_year, kpi_ids=kpi_ids)


@data_bp.route("/img/<int:kpi_id>")
def serve_kpi_image(kpi_id):
    """
    Serve KPI images from the static/img folder
    GET /img/<kpi_id>
    
    Returns:
        Image file or 404 if not found
    """
    from flask import send_from_directory
    import os
    
    img_path = os.path.join(current_app.static_folder, 'img', f'{kpi_id}.png')
    
    if os.path.exists(img_path):
        return send_from_directory(os.path.join(current_app.static_folder, 'img'), f'{kpi_id}.png')
    else:
        # Return a default "no image" placeholder
        no_image_path = os.path.join(current_app.static_folder, 'img', 'no-image.jpg')
        if os.path.exists(no_image_path):
            return send_from_directory(os.path.join(current_app.static_folder, 'img'), 'no-image.jpg')
        else:
            return jsonify({"status": "error", "message": "Image not found"}), 404

@data_bp.route("/api/goals", methods=["GET"])
def get_goals():
    """
    Get KPI goals for a specific year and its previous year
    GET /api/goals?year=2026
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    year = request.args.get("year", datetime.now().year, type=int)
    prev_year = year - 1

    query = text("""
        SELECT 
            act.kpi_id,
            act.activities,
            act.unit,
            g_prev.target AS prev_target,
            g_curr.target AS curr_target
        FROM public.activities act
        LEFT JOIN public.goals g_prev ON act.kpi_id = g_prev.kpi_id AND g_prev.year = :prev_year
        LEFT JOIN public.goals g_curr ON act.kpi_id = g_curr.kpi_id AND g_curr.year = :curr_year
        ORDER BY CAST(act.kpi_id AS INTEGER) ASC;
    """)

    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            result = conn.execute(query, {"prev_year": prev_year, "curr_year": year})
            data = [dict(row._mapping) for row in result]
            
            # Convert decimal to float for JSON
            for row in data:
                if row['prev_target'] is not None:
                    row['prev_target'] = float(row['prev_target'])
                if row['curr_target'] is not None:
                    row['curr_target'] = float(row['curr_target'])

            return jsonify({
                "status": "success", 
                "year": year, 
                "prev_year": prev_year, 
                "data": data
            }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route("/api/goals/batch-save", methods=["POST"])
def batch_save_goals():
    """
    Save multiple KPI goals for a year
    POST /api/goals/batch-save
    """
    from services.sync_service import get_pg_engine
    from sqlalchemy import text

    try:
        payload = request.get_json()
        year = payload.get("year")
        goals = payload.get("goals", [])

        if not year or not goals:
            return jsonify({"status": "error", "message": "Missing year or goals"}), 400

        engine = get_pg_engine()
        with engine.connect() as conn:
            query = text("""
                INSERT INTO public.goals (kpi_id, year, target)
                VALUES (:kpi_id, :year, :target)
                ON CONFLICT (kpi_id, year) 
                DO UPDATE SET target = EXCLUDED.target
            """)

            for item in goals:
                # Handle empty strings or nulls
                target = item.get("target")
                if target == "" or target is None:
                    target = None
                else:
                    target = float(target)

                conn.execute(query, {
                    "kpi_id": item["kpi_id"],
                    "year": year,
                    "target": target
                })
            conn.commit()

        return jsonify({"status": "success", "message": f"Successfully saved {len(goals)} targets"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@data_bp.route("/settings")
def settings_kpis():
    from services.sync_service import get_pg_engine
    from sqlalchemy import text
    try:
        engine = get_pg_engine()
        with engine.connect() as conn:
            # 1. Get the list of all KPIs with their current settings
            kpi_settings_query = text("""
                SELECT 
                    a.kpi_id, 
                    a.group_id, 
                    a.department_id, 
                    a."no", 
                    a.sub_no, 
                    a.activities, 
                    a.description, 
                    a.description2, 
                    a."source", 
                    a."linkUrl", 
                    a.unit, 
                    a.source_result, 
                    a.istarget, 
                    a.active,
                    d.department_desc,
                    g.group_desc
                FROM public.activities a
                LEFT JOIN public.department d ON a.department_id = d.department_id
                LEFT JOIN public."group" g ON a.group_id = g.group_id
                ORDER BY a.kpi_id
            """)
            result = conn.execute(kpi_settings_query)
            kpis = [dict(row._mapping) for row in result]
            
            # 2. Get all departments and groups for dropdowns
            departments_result = conn.execute(text("SELECT department_id, department_desc FROM public.department ORDER BY department_id"))
            departments = [dict(row._mapping) for row in departments_result]
            
            groups_result = conn.execute(text('SELECT group_id, group_desc FROM public."group" ORDER BY group_id'))
            groups = [dict(row._mapping) for row in groups_result]
            
            return render_template("setting.html", 
                                   kpis=kpis, 
                                   departments=departments, 
                                   groups=groups)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
        

@data_bp.route("/settings/save-kpi", methods=["POST"])
def save_kpi():
    from services.sync_service import get_pg_engine
    from sqlalchemy import text
    try:
        data = request.json
        kpi_id = data.get('kpi_id')
        
        engine = get_pg_engine()
        with engine.begin() as conn:
            # Update activities table
            update_query = text("""
                UPDATE public.activities 
                SET 
                    group_id = :group_id,
                    department_id = :department_id,
                    activities = :activities,
                    description = :description,
                    unit = :unit,
                    "linkUrl" = :linkUrl,
                    active = CAST(:active AS bit)
                WHERE kpi_id = :kpi_id
            """)
            conn.execute(update_query, {
                "group_id": data.get('group_id'),
                "department_id": data.get('department_id'),
                "activities": data.get('activities'),
                "description": data.get('description'),
                "unit": data.get('unit'),
                "linkUrl": data.get('linkUrl'),
                "active": '1' if data.get('active') else '0',
                "kpi_id": kpi_id
            })
            
            # (Removed update to public.kpis as table does not exist)
            
        return jsonify({"status": "success", "message": "KPI updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error saving KPI: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@data_bp.route("/settings/add-kpi", methods=["POST"])
def add_kpi():
    from services.sync_service import get_pg_engine
    from sqlalchemy import text
    try:
        data = request.json
        kpi_id = data.get('kpi_id')
        
        engine = get_pg_engine()
        with engine.begin() as conn:
            # Check if KPI ID already exists
            check = conn.execute(text("SELECT kpi_id FROM public.activities WHERE kpi_id = :kpi_id"), {"kpi_id": kpi_id}).fetchone()
            if check:
                return jsonify({"status": "error", "message": f"KPI ID {kpi_id} already exists"}), 400
                
            # Insert into activities table
            insert_query = text("""
                INSERT INTO public.activities (
                    kpi_id, group_id, department_id, activities, description, unit, "linkUrl", active, istarget
                ) VALUES (
                    :kpi_id, :group_id, :department_id, :activities, :description, :unit, :linkUrl, CAST(:active AS bit), 'Y'
                )
            """)
            conn.execute(insert_query, {
                "kpi_id": kpi_id,
                "group_id": data.get('group_id'),
                "department_id": data.get('department_id'),
                "activities": data.get('activities'),
                "description": data.get('description'),
                "unit": data.get('unit'),
                "linkUrl": data.get('linkUrl'),
                "active": '1' if data.get('active', True) else '0'
            })
            
        return jsonify({"status": "success", "message": "KPI added successfully"}), 201
    except Exception as e:
        logger.error(f"Error adding KPI: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500





# SELECT kpi_id, group_id, department_id, no, sub_no, activities, description, description2, source, \"linkUrl\", unit, source_result, istarget, active
# 	FROM public.activities;

