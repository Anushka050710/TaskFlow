from flask import Blueprint, jsonify
from ..database import db
from sqlalchemy import text

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """Liveness + readiness probe."""
    try:
        db.session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:
        db_status = f"error: {exc}"

    status = "ok" if db_status == "ok" else "degraded"
    return jsonify({"status": status, "db": db_status}), 200 if status == "ok" else 503
