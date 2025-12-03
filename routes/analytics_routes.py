'''Author: Samiul Ahamed Fhyas'''
from flask import Blueprint
from controllers.analytics_controller import AnalyticsController

analytics_bp = Blueprint("analytics_bp", __name__, url_prefix="/api/analytics")


@analytics_bp.get("/stats")
def get_stats():
    """Get analytics statistics."""
    return AnalyticsController.get_stats()
