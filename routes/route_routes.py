'''Author: Samiul Ahamed Fhyas'''
from flask import Blueprint, request
from controllers.route_controller import RouteController

route_bp = Blueprint("route_bp", __name__, url_prefix="/api/routes")


@route_bp.get("/search")
def search_routes():
    """
    Search for bus routes based on query parameters.

    Query Parameters:
        from/src (str): Source location (required)
        to/dst (str): Destination location (required)
        date/travel_date (str): Travel date (required)
        bus_type/type (str, optional): Filter by bus type
        operator (str, optional): Filter by operator
        price_min (float, optional): Minimum fare
        price_max (float, optional): Maximum fare
        sort_by (str, optional): Sort criteria

    Returns:
        JSON response with buses list and suggestions.
    """
    return RouteController.search(request.args)


@route_bp.get("/seat-layout/<int:route_id>")
def seat_layout(route_id: int):
    """
    Get seat layout for a specific bus route.

    Args:
        route_id (int): The ID of the bus route.

    Query Parameters:
        date (str): Travel date (required)

    Returns:
        JSON response with route details and seat layout.
    """
    travel_date = request.args.get("date") or ""
    if not travel_date:
        return {"message": "date is required"}, 400
    return RouteController.seat_layout(route_id, travel_date)


@route_bp.get("/meta")
def routes_meta():
    """
    Get metadata about distinct stations and operators.

    Returns:
        JSON response with lists of stations and operators.
    """
    return RouteController.meta()


@route_bp.get("/all")
def routes_all():
    """
    Get all bus routes with enriched data.

    Returns:
        JSON response with list of all bus routes.
    """
    return RouteController.all_routes()
